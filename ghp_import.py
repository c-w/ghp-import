#! /usr/bin/env python

import errno
import optparse as op
import os
import subprocess as sp
import sys
import time
from dateutil import tz
from datetime import datetime

try:
    from shlex import quote
except ImportError:
    from pipes import quote

__all__ = ['ghp_import']

__usage__ = "%prog [OPTIONS] DIRECTORY"


class GhpError(Exception):
    def __init__(self, message):
        self.message = message


if sys.version_info[0] == 3:
    def enc(text):
        if isinstance(text, bytes):
            return text
        return text.encode()

    def dec(text):
        if isinstance(text, bytes):
            return text.decode('utf-8')
        return text

    def write(pipe, data):
        try:
            pipe.stdin.write(data)
        except IOError as e:
            if e.errno != errno.EPIPE:
                raise
else:
    def enc(text):
        if isinstance(text, unicode):  # noqa F821
            return text.encode('utf-8')
        return text

    def dec(text):
        if isinstance(text, unicode):  # noqa F821
            return text
        return text.decode('utf-8')

    def write(pipe, data):
        pipe.stdin.write(data)


class Git(object):
    def __init__(self, use_shell=False):
        self.use_shell = use_shell

        self.cmd = None
        self.pipe = None
        self.stderr = None
        self.stdout = None

    def check_repo(self):
        if self.call('rev-parse') != 0:
            error = self.stderr
            if not error:
                error = "Unknown Git error"
            error = dec(error)
            if error.startswith("fatal: "):
                error = error[len("fatal: "):]
            raise GhpError(error)

    def try_rebase(self, remote, branch):
        rc = self.call('rev-list', '--max-count=1', '%s/%s' % (remote, branch))
        if rc != 0:
            return True
        rev = dec(self.stdout.strip())
        rc = self.call('update-ref', 'refs/heads/%s' % branch, rev)
        if rc != 0:
            return False
        return True

    def get_config(self, key):
        self.call('config', key)
        return self.stdout.strip()

    def get_prev_commit(self, branch):
        rc = self.call('rev-list', '--max-count=1', branch, '--')
        if rc != 0:
            return None
        return dec(self.stdout).strip()

    def open(self, *args, **kwargs):
        if self.use_shell:
            self.cmd = 'git ' + ' '.join(map(quote, args))
        else:
            self.cmd = ['git'] + list(args)
        if sys.version_info >= (3, 2, 0):
            kwargs['universal_newlines'] = False
        for k in 'stdin stdout stderr'.split():
            kwargs.setdefault(k, sp.PIPE)
        kwargs['shell'] = self.use_shell
        self.pipe = sp.Popen(self.cmd, **kwargs)
        return self.pipe

    def call(self, *args, **kwargs):
        self.open(*args, **kwargs)
        (self.stdout, self.stderr) = self.pipe.communicate()
        return self.pipe.wait()

    def check_call(self, *args, **kwargs):
        kwargs["shell"] = self.use_shell
        sp.check_call(['git'] + list(args), **kwargs)


def mk_when(timestamp=None):
    if timestamp is None:
        timestamp = int(time.time())
    currtz = datetime.now(tz.tzlocal()).strftime('%z')
    return "%s %s" % (timestamp, currtz)


def start_commit(pipe, git, branch, message):
    uname = os.getenv('GIT_COMMITTER_NAME', dec(git.get_config('user.name')))
    email = os.getenv('GIT_COMMITTER_EMAIL', dec(git.get_config('user.email')))
    when = os.getenv('GIT_COMMITTER_DATE', mk_when())
    write(pipe, enc('commit refs/heads/%s\n' % branch))
    write(pipe, enc('committer %s <%s> %s\n' % (uname, email, when)))
    write(pipe, enc('data %d\n%s\n' % (len(enc(message)), message)))
    head = git.get_prev_commit(branch)
    if head:
        write(pipe, enc('from %s\n' % head))
    write(pipe, enc('deleteall\n'))


def add_file(pipe, srcpath, tgtpath):
    with open(srcpath, "rb") as handle:
        if os.access(srcpath, os.X_OK):
            write(pipe, enc('M 100755 inline %s\n' % tgtpath))
        else:
            write(pipe, enc('M 100644 inline %s\n' % tgtpath))
        data = handle.read()
        write(pipe, enc('data %d\n' % len(data)))
        write(pipe, enc(data))
        write(pipe, enc('\n'))


def add_nojekyll(pipe):
    write(pipe, enc('M 100644 inline .nojekyll\n'))
    write(pipe, enc('data 0\n'))
    write(pipe, enc('\n'))


def add_cname(pipe, cname):
    write(pipe, enc('M 100644 inline CNAME\n'))
    write(pipe, enc('data %d\n%s\n' % (len(enc(cname)), cname)))


def gitpath(fname):
    norm = os.path.normpath(fname)
    return "/".join(norm.split(os.path.sep))


def run_import(git, srcdir, **opts):
    srcdir = dec(srcdir)
    pipe = git.open('fast-import', '--date-format=raw', '--quiet',
                    stdin=sp.PIPE, stdout=None, stderr=None)
    start_commit(pipe, git, opts['branch'], opts['mesg'])
    for path, _, fnames in os.walk(srcdir, followlinks=opts['followlinks']):
        for fn in fnames:
            fpath = os.path.join(path, fn)
            gpath = gitpath(os.path.relpath(fpath, start=srcdir))
            if opts['prefix']:
                gpath = os.path.join(opts['prefix'], gpath)
            add_file(pipe, fpath, gpath)
    if opts['nojekyll']:
        add_nojekyll(pipe)
    if opts['cname'] is not None:
        add_cname(pipe, opts['cname'])
    write(pipe, enc('\n'))
    pipe.stdin.close()
    if pipe.wait() != 0:
        sys.stdout.write(enc("Failed to process commit.\n"))


def options():
    return [
        op.make_option(
            '-n', '--no-jekyll', dest='nojekyll', default=False,
            action="store_true",
            help='Include a .nojekyll file in the branch.'),
        op.make_option(
            '-c', '--cname', dest='cname', default=None,
            help='Write a CNAME file with the given CNAME.'),
        op.make_option(
            '-m', '--message', dest='mesg',
            default='Update documentation',
            help='The commit message to use on the target branch.'),
        op.make_option(
            '-p', '--push', dest='push', default=False,
            action='store_true',
            help='Push the branch to origin/{branch} after committing.'),
        op.make_option(
            '-x', '--prefix', dest='prefix', default=None,
            help='The prefix to add to each file that gets pushed to the '
                 'remote. [%default]'),
        op.make_option(
            '-f', '--force', dest='force',
            default=False, action='store_true',
            help='Force the push to the repository'),
        op.make_option(
            '-r', '--remote', dest='remote', default='origin',
            help='The name of the remote to push to. [%default]'),
        op.make_option(
            '-b', '--branch', dest='branch', default='gh-pages',
            help='Name of the branch to write to. [%default]'),
        op.make_option(
            '-s', '--shell', dest='use_shell', default=False,
            action='store_true',
            help='Use the shell when invoking Git. [%default]'),
        op.make_option(
            '-l', '--follow-links', dest='followlinks',
            default=False, action='store_true',
            help='Follow symlinks when adding files. [%default]')
    ]


def ghp_import(srcdir, **kwargs):
    if not os.path.isdir(srcdir):
        raise GhpError("Not a directory: %s" % srcdir)

    opts = {opt.dest: opt.default for opt in options()}
    opts.update(kwargs)

    git = Git(use_shell=opts['use_shell'])
    git.check_repo()

    if not git.try_rebase(opts['remote'], opts['branch']):
        raise GhpError("Failed to rebase %s branch." % opts['branch'])

    run_import(git, srcdir, **opts)

    if opts['push']:
        if opts['force']:
            git.check_call('push', opts['remote'], opts['branch'], '--force')
        else:
            git.check_call('push', opts['remote'], opts['branch'])


def main():
    parser = op.OptionParser(usage=__usage__, option_list=options())
    opts, args = parser.parse_args()

    if len(args) == 0:
        parser.error("No import directory specified.")

    if len(args) > 1:
        parser.error("Unknown arguments specified: %s" % ', '.join(args[1:]))

    try:
        ghp_import(args[0], **opts.__dict__)
    except GhpError as e:
        parser.error(e.message)


if __name__ == '__main__':
    main()
