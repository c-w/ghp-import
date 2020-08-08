GitHub Pages Import
===================

[![CI status](https://github.com/davisp/ghp-import/workflows/CI/badge.svg)](https://github.com/davisp/ghp-import/actions?query=workflow%3Aci)
[![CircleCI](https://circleci.com/gh/c-w/ghp-import/tree/master.svg?style=svg)](https://circleci.com/gh/c-w/ghp-import/tree/master)
[![TravisCI](https://travis-ci.org/c-w/ghp-import.svg?branch=master)](https://travis-ci.org/c-w/ghp-import)
[![AzureDevOps](https://clewolff.visualstudio.com/ghp-import/_apis/build/status/c-w.ghp-import?branchName=master)](https://clewolff.visualstudio.com/ghp-import/_build/latest?definitionId=10&branchName=master)

As part of [gunicorn][gunicorn], [Benoit Chesneau][benoit] and I have been
starting to look at how to host documentation. There's the obvious method of
using [GitHub's post-receive hook][github-post] to trigger doc builds and rsync
to a webserver, but we ended up wanting to try out github's hosting to make the
whole interface a bit more robust.

[GitHub Pages][gh-pages] is a pretty awesome service that GitHub provides for
hosting project documentation. The only thing is that it requires a
`gh-pages` branch that is the site's document root. This means that keeping
documentation sources in the branch with code is a bit difficult. And it really
turns into a head scratcher for things like [Sphinx][sphinx] that want to
access documentation sources and code sources at the same time.

Then I stumbled across an interesting looking package called
[github-tools][github-tools] that looked almost like what I wanted. It was a tad
complicated and more involved than I wanted but it gave me an idea. Why not
just write a script that can copy a directory to the `gh-pages` branch of the
repository. This saves me from even having to think about the branch and
everything becomes magical.

This is what `ghp-import` was written for.

[gunicorn]: http://www.gunicorn.com/ "Gunicorn"
[benoit]: http://github.com/benoitc "Benoît Chesneau"
[github-post]: https://help.github.com/articles/post-receive-hooks "GitHub Post-Receive Hook"
[gh-pages]: http://pages.github.com/ "GitHub Pages"
[sphinx]: http://sphinx.pocoo.org/ "Sphinx Documentation"
[github-tools]: http://dinoboff.github.com/github-tools/ "github-tools"


Big Fat Warning
---------------

This will **DESTROY** your `gh-pages` branch. If you love it, you'll want to
take backups before playing with this. This script assumes that `gh-pages` is
100% derivative. You should never edit files in your `gh-pages` branch by hand
if you're using this script because you will lose your work.

Usage
-----

```
Usage: ghp-import [OPTIONS] DIRECTORY

Options:
  -n, --no-jekyll       Include a .nojekyll file in the branch.
  -c CNAME, --cname=CNAME
                        Write a CNAME file with the given CNAME.
  -m MESG, --message=MESG
                        The commit message to use on the target branch.
  -p, --push            Push the branch to origin/{branch} after committing.
  -x PREFIX, --prefix=PREFIX
                        The prefix to add to each file that gets pushed to the
                        remote. [none]
  -f, --force           Force the push to the repository
  -r REMOTE, --remote=REMOTE
                        The name of the remote to push to. [origin]
  -b BRANCH, --branch=BRANCH
                        Name of the branch to write to. [gh-pages]
  -s, --shell           Use the shell when invoking Git. [False]
  -l, --follow-links    Follow symlinks when adding files. [False]
  -h, --help            show this help message and exit
```

Its pretty simple. Inside your repository just run `ghp-import $DOCS_DIR`
where `$DOCS_DIR` is the path to the **built** documentation. This will write a
commit to your `gh-pages` branch with the current documents in it.

If you specify `-p` it will also attempt to push the `gh-pages` branch to
GitHub. By default it'll just run `git push origin gh-pages`. You can specify
a different remote using the `-r` flag.

You can specify a different branch with `-b`. This is useful for user and
organization page, which are served from the `master` branch.

Some Windows users report needing to pass Git commands through the shell which can be accomplished by passing `-s`.

The `-l` option will cause the import to follow symlinks for users that have odd configurations that include symlinking outside of their documentation directory.

Python Usage
------------

You can also call ghp_import directly from your Python code as a library. The
library has one public function `ghp_import.ghp_import`, which accepts the
following arguments:

* `srcdir`: The path to the **built** documentation (required).
* `remote`: The name of the remote to push to. Default: `origin`.
* `branch`: Name of the branch to write to. Default: `gh-pages`.
* `mesg`: The commit message to use on the target branch. Default: `Update documentation`.
* `push`: Push the branch to {remote}/{branch} after committing. Default: `False`.
* `prefix`: The prefix to add to each file that gets pushed to the remote. Default: `None`.
* `force`: Force the push to the repository. Default: `False`.
* `use_shell`: Default: Use the shell when invoking Git. `False`.
* `followlinks`: Follow symlinks when adding files. Default: `False`.
* `cname`: Write a CNAME file with the given CNAME. Default: `None`.
* `nojekyll`: Include a .nojekyll file in the branch. Default: `False`.

With Python's current working directory (cwd) inside your repository, do the
following:

```python
from ghp_import import ghp_import
ghp_import('docs', push=True, cname='example.com')
```

License
-------

`ghp-import` is distributed under the Tumbolia Public License. See the LICENSE
file for more information.
