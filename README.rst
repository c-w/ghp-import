GitHub Pages Import
===================

As part of gunicorn_, me and `Benoit Chesneau`_ have been starting to look at
how to host documentation. There's the obvious method of using GitHub_'s
post-update hooks to trigger doc builds and rsync to a webserver, but we ended
up wanting to try out github's hosting to make the whole interface a bit more
robust.

`GitHub Pages`_ is a pretty awesome service that GitHub provides for hosting
project documentation. The only thing is that it requires a ``gh-pages`` branch
that is the site's document root. This means that keeping documentation sources
in the branch with code is a bit difficult. And it really turns into a head
scratcher for things like Sphinx_ that want to access documentation sources and
code sources at the same time.

Then I stumbled across an interesting looking package called `github-tools`_
that looked almost like what I wanted. It was a tad complicated and more
involved than I wanted but it gave me an idear. Why not just write a script that
can copy a directory to the ``gh-pages`` branch of the repository. This saves me
from even having to think about the branch and everything becomes magical.

This is what ``ghp-import`` was written for.

.. _gunicorn: http://www.gunicorn.com/
.. _`Benoit Chesneau`: http://github.com/benoitc
.. _GitHub: http://github.com/
.. _`GitHub Pages`: http://pages.github.com/
.. _Sphinx: http://sphinx.pocoo.org/
.. _`github-tools`: http://dinoboff.github.com/github-tools/

Big Fat Warning
---------------

This will **DESTROY** your gh-pages branch. If you love it, you'll want to take
backups before playing with this. This script assumes that gh-pages is 100%
derivative. You should never edit files in your gh-pages branch by hand if
you're using this script because you will lose your work.

Usage
-----

::

    Usage: ghp-import [OPTIONS] DIRECTORY

    Options:
      -m MESG     The commit message to use on the target branch.
      -p          Push the branch to origin/{branch} after committing.
      -r REMOTE   The name of the remote to push to. [origin]
      -b BRANCH   Name of the branch to write to. [gh-pages]
      -h, --help  show this help message and exit

Its pretty simple. Inside your repository just run ``ghp-import $DOCS_DIR``
where ``$DOCS_DIR`` is the path to the *built* documentation. This will write a
commit to your ``gh-pages`` branch with the current documents in it.

If you specify ``-p`` it will also attempt to push the ``gh-pages`` branch to
GitHub. By default it'll just run ``git push origin gh-pages``. You can specify
a different remote using the ``-r`` flag.

You can specify a different branch with ``-b``. This is useful for user and
organization page, which are served from the ``master`` branch.

License
-------

ghp-import is distributed under the Tumbolia Public License. See the LICENSE
file for more information.
