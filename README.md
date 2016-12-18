GitHub Pages Import
===================

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
complicated and more involved than I wanted but it gave me an idear. Why not
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

    Usage: ghp-import [OPTIONS] DIRECTORY

	Options:
	  -n          Include a .nojekyll file in the branch.
	  -c CNAME    Write a CNAME file with the given CNAME.
	  -m MESG     The commit message to use on the target branch.
	  -p          Push the branch to origin/{branch} after committing.
	  -f          Force the push to the repository
	  -r REMOTE   The name of the remote to push to. [origin]
	  -b BRANCH   Name of the branch to write to. [gh-pages]
	  -s          Use the shell when invoking Git. [False]
	  -l          Follow symlinks when adding files. [False]
	  -h, --help  show this help message and exit

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

License
-------

`ghp-import` is distributed under the Tumbolia Public License. See the LICENSE
file for more information.
