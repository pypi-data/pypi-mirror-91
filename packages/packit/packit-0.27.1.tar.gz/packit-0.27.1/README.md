# PacKit

_Contents:_
- [Rationale](#rationale)
- [Overview](#overview)
- [Usage](#usage)
- [Facilities](#facilities)
- [Including Files Other than Python Libraries](#including-files)
- [Further Development](#development)

<a name="rationale"></a>
## Rationale

Creating python packages is routine operation that involves a lot of
actions that could be automated. Although there are petty good tools
like [pbr](http://docs.openstack.org/developer/pbr/) for that purpose,
they miss some features and lack flexibility by trying to enforce some
strongly opinionated decisions upon you. PacKit tries to solve this by
providing a simple, convenient, and flexible way to create and build
packages while aiming for following goals:

  - simple declarative way to configure your package through `setup.cfg`
    following [distutils2 setup.cfg
    syntax](http://alexis.notmyidea.org/distutils2/setupcfg.html)
  - reasonable defaults
  - open for extension

<a name="overview"></a>
## Overview

PacKit is wrapper around [pbr](http://docs.openstack.org/developer/pbr/)
though it only uses it for interaction with setuptools/distutils through
simplified interface. None of
[pbr](http://docs.openstack.org/developer/pbr/) functions are exposed
but instead PacKit provides its own interface.

### Available facilities

Here's a brief overview of currently implemented facilities and the list
will be extended as new ones will be added.

  - **auto-version** - set package version depending on selected
    versioning strategy.
  - **auto-description** - set package long description
  - **auto-license** - include license file into distribution
  - **auto-dependencies** - populate `install_requires` and
    *test\_requires* from requirement files
  - **auto-packages** - discover packages to include in distribution.
  - **auto-extra-meta** - add useful options to the metadata config
    section
  - **auto-package-data** - include all files tracked by `git` from
    package dirs only.
  - **auto-tests** - make `python setup.py test` run tests with `tox` or
    `pytest` (depending on `tox.ini` presence).

On top of that PacKit forces easy\_install to honor following [PIP's
fetch
directives](https://pip.pypa.io/en/latest/user_guide.html#configuration):

  - index\_url
  - find\_links

### Planned facilities

  - **auto-plate** - integration with
    [platter](http://platter.pocoo.org/)
  - **auto-license** - fill out license information
  - **auto-pep8** - produce style-check reports
  - **auto-docs** - API docs generation
  - **auto-clean** - configurable clean jobs
  - **auto-coverage** (?) - produce coverage reports while running tests

If you don't see desired facilities or have cool features in mind feel
free to contact us and tell about your ideas.

<a name="usage"></a>
## Usage

Create a `setup.py` in your project dir: :

    from setuptools import setup
    
    setup(setup_requires='packit', packit=True)

That was the first and the last time you touched that file for your
project.

Now let's create a `setup.cfg` that you will use in order to configure
your package:

    [metadata]
    name = cool-package

And... if you're not doing anything tricky in your package then that's
enough\! And if you do, take a look at the section below.

<a name="facilities"></a>
## Facilities

Currently all available facilities are enabled by default. Though you
can easily turn them off by using `facilities` section in your
`setup.cfg`:

    [facilities]
    auto-version = 0
    auto-dependencies = f
    auto-packages = false
    auto-package-data = n
    auto-tests = no

If facility is explicitly disabled it won't be used even if
facility-specific configuration section is present.

Facility-specific defaults and configuration options described below.

### auto-version

When enabled, `auto-version` will generate and set package version
according to selected versioning strategy.

Versioning strategy can be selected using `type` field under
`auto-version` section within `setup.cfg`. The default is:

    [auto-version]
    type = git-pep440
    output = src/templates/version.html

You can use `output` field to ask PacKit to write generated version
value into specified filename. The specified filename do not need to
exist but the parent directories should exist. Provided path should
always use forward slashes.

#### git-pep440

Generate [PEP440](https://www.python.org/dev/peps/pep-0440/)-compliant
version from **annotated** `git` tags. It's expected that you are using
git tags that follow [public version
identifier](https://www.python.org/dev/peps/pep-0440/#public-version-identifiers)
description and `git-pep440` will just append number of commits since
tag was applied to your tag value (the `N` in [public version
identifier](https://www.python.org/dev/peps/pep-0440/#public-version-identifiers)
description).

If number of commits since tag equal to 0 (your building the tagged
version) the `N` value won't be appended. Otherwise, it will be appended
and [local version
identifier](https://www.python.org/dev/peps/pep-0440/#local-version-identifiers)
equal to first 7 chars of commit hash will be also added.

Please note: you must create an **annotated** tag, otherwise it will be
ignored.

Example: 1. \<git tag -a 1.2.3.dev -m "dev release 1.2.3.dev"\> -\>
version is `1.2.3.dev`

2.  \<git commit\> -\> version is `1.2.3.dev.post1`
3.  \<git commit\> -\> version is `1.2.3.dev.post2`
4.  \<git tag -a 1.2.3.a -m "Release 1.2.3.a"\> -\> version is `1.2.3.a`
5.  \<git commit\> -\> version is `1.2.3.a.post1`
6.  \<git tag -a 1.2.3 -m "Release 1.2.3"\> -\> version is `1.2.3`
7.  \<git commit\> -\> version is `1.2.3.post1`
8.  \<git commit\> -\> version is `1.2.3.post2`

#### fixed

Use value specified in `value` (it's required when this strategy is
used) under `auto-version` section in `setup.cfg`:

    [auto-version]
    type = fixed
    value = 3.3

#### file

Read a line using UTF-8 encoding from the file specified in `value`
(it's required when this strategy is used) under `auto-version` section
in `setup.cfg`, strip it and use as a version.

    [auto-version]
    type = file
    value = VERSION.txt

#### shell

Execute command specified in `value` (it's required when this strategy
is used) under `auto-version` section in `setup.cfg`, read a line from
`stdout`, strip it and use as a version

#### composite

The most advanced version strategy designed for special cases. It allows
you to generate complex version values based on other version
strategies. The usage is pretty simple though:

    [auto-version]
    type = composite
    value = {foo}.{bar}+{git}
    output = main.version
    
    [auto-version:foo]
    type = fixed
    value = 42
    output = 1st.version
    
    [auto-version:bar]
    type = shell
    value = echo $RANDOM
    
    [auto-version:git]
    type = git-pep440
    output = 3rd.version

The `value` field in composite version strategy should be a valid
[string format
expression](https://docs.python.org/2/library/string.html#string-formatting).

Please note that `output` directives used here only for reference (to
show that they can be used anywhere) and are not required.

It's OK to define 'extra' version components and not use them but it's
an error to not define any of components mentioned in composite version
template.

### auto-description

When enabled will fill out `long_description` for package from a readme.

The `readme` file name could be specified with `file` field under
`auto-description` section.

If no file name provided, it will be discovered automatically by trying
following list of files:

  - README
  - readme
  - CHANGELOG
  - changelog

Each of these files will be tried with following extensions:

  - \<without extension\>
  - .md
  - .markdown
  - .mkdn
  - .text
  - .rst
  - .txt

The readme file will be included in the package data.

### auto-license

When enabled will include the license file into the distribution.

The license file name could be specified by the `file` field within
`auto-license` section.

If license file name is not provided the facility will try to discover
it in the current dir trying following file names:

  - LICENSE
  - license

Each of these files will be tried with following extensions:

  - \<without extension\>
  - .md
  - .markdown
  - .mkdn
  - .text
  - .rst
  - .txt

### auto-dependencies

When enabled will fill `install_requires` and `test_requires` from
requirement files.

Requirement files could be specified by `install` and `test` fields
under the `auto-dependencies` section of the `setup.cfg`.

If requirements file names not provided then the facility will try to
discover them automatically.

For installation requirements following paths will be tried:

  - requires
  - requirements
  - requirements/prod
  - requirements/release
  - requirements/install
  - requirements/main
  - requirements/base

For testing requirements following paths will be tried:

  - test-requires
  - test\_requires
  - test-requirements
  - test\_requirements
  - requirements\_test
  - requirements-test
  - requirements/test

For each path following extensions will be tried

  - \<without extension\>
  - .pip
  - .txt

Once a file is found, PacKit stops looking for more files.

**You can use vcs project urls and/or archive urls/paths** as described
in [pip
usage](https://pip.pypa.io/en/latest/reference/pip_install.html#usage) -
they will be split in dependency links and package names during package
creation and will be properly handled by pip/easyinstall during
installation. Remember that you can also make "includes" relationships
between `requirements.txt` files by including a line like `-r
other-requires-file.txt`.

### auto-packages

When enabled and no packages provided in `setup.cfg` through `packages`
option under `files` section will try to automatically find out all
packages in current dir recursively.

It operates using `exclude` and `include` values that can be specified
under `auto-packages` section within `setup.cfg`.

If `exclude` not provided the following defaults will be used: `test`,
`docs`, `.tox` and `env`.

If `include` not provided, `auto-packages` will try the following steps
in order to generate it:

1.  If `packages_root` value provided under `files` section in
    `setup.cfg`, it will be used.
2.  Otherwise the current working dir will be scanned for any python
    packages (dirs with \_\_init\_\_.py) while honoring exclude `value`.
    *This packages also will be included into the resulting list of
    packages.*

Once `include` value is determined, the resulting packages list will be
generated using following algorithm:

    for path in include:
        found_packages |= set(find_packages(path, exclude))

### auto-extra-meta

When enabled, adds a number of additional options to 'metadata' section.

Right now, only 1 extra option supported:

  - **is\_pure** - allows you to override 'purity' flag for
    distribution, i.e. you can explicitly say whether your distribution
    is platform-specific or no.

### auto-tests

Has no additional configuration options \[yet\].

When enabled, the `python setup.py test` is equal to running:

  - **tox** if `tox.ini` is present
  - **pytest** with
    [pytest-gitignore](https://pypi.python.org/pypi/pytest-gitignore/)
    and
    [teamcity-messages](https://pypi.python.org/pypi/teamcity-messages/)
    plugins enabled by default otherwise (if you need any other plugins
    just add them to test requirements) and activate them with
    additional options (see below)

The facility automatically downloads underlying test framework and
install it - you don't need to worry about it.

You can pass additional parameters to the underlying test framework with
'-a' or '--additional-test-args='.

### auto-package-data

See the next section.

<a name="including-files"></a>
## Including Files Other than Python Libraries

Often, you need to include a data file, or another program, or some
other kind of file, with your Python package. Here are a number of
common situations, and how to accomplish them using packit:

### Placing data files with the code that uses them: auto-package-data

The default is that the `auto-package-data` facility is enabled. In this
configuration, you can include data files for your python library very
easily by just:

  - Placing them inside a Python package directory (so next to an `__init__.py`
    or in a subdirectory), and
  - Adding them to git version control.

```
setup.cfg
src/
src/nicelib/
src/nicelib/__init__.py
src/nicelib/things.py
src/nicelib/somedata.csv
```

__No change in setup.cfg is required.__ Putting the files here will cause the
packaging system to notice them and install them in the same arrangement next
to your Python files, but inside the virtualenv where your package is
installed.

Once this is done, you have several easy options for accessing them, and all of
these should work the same way in development and once installed:
* The least magical way is `pathlib.Path(__file__).parent / 'somedata.csv'`,
  or some equivalent with `os.path` calls.  This makes your package non-zip-safe,
  so it can't be used in a `pex` or `zipapp` application.
* The new hotness is `importlib.resources.open_text('nicelib',
  'somedata.csv')` and [related
  functions](https://docs.python.org/3/library/importlib.html#module-importlib.resources),
  available in the stdlib in Python 3.7+ or as a backport in the
  `importlib_resources` PyPI package.  One limitation is this does *not*
  support putting resources deeper in subdirectories.
* The previous standard has been `pkg_resources.resource_stream('nicelib',
  'somedata.csv')` and [related
  functions](https://setuptools.readthedocs.io/en/latest/pkg_resources.html#basic-resource-access).
  This supports deeper subdirectories, but is *much* slower than
  `importlib.resources`.  You shouldn't need to install `pkg_resources`,
  it's part of `setuptools`, which is always available these days.

You can turn off the `auto-package-data` facility if you **don't** want this
file inclusion mechanism to happen:

    [facilities]
    auto-package-data = no

`auto-package-data` will not work if your Python package is not at the
root of your git repository (`setup.py` is not next to `.git`).

### Placing data files relative to the virtual environment

You can also place files relative to the virtualenv, rather than inside
the package hierarchy (which would be in
`virtualenv/lib/python*/site-packages/something`). This is often used
for things like static files in a Django project, so that they are easy
to find for an external web server. The syntax for this is:

    [files]
    data_files =
        dest_dir = src_dir/**
        dest_dir = file_to_put_there

In this example, `dest_dir` will be created within the top level of the
virtualenv. The contents of `src_dir` will be placed inside it, along
with `file_to_put_there`.

If you need to include a **compiled executable file** in your package, this
is a convenient way to do it - include `bin = bin/**` for example. See
the `fastatools` package for an example of this.  There is also a
[confluence page with more details on including compiled
programs](https://confluence.ncbi.nlm.nih.gov/x/TVA0Aw).

### Including Python scripts

Scripts need to be treated specially, and not just dropped into `bin`
using `data_files`, because Python changes the shebang (`#!`) line to
match the virtualenv's python interpreter. This means you can directly
run a script without activating a virtualenv - e.g. `env/bin/pip install
attrs` will work even if `env` isn't activated.\[1\]

If you have some scripts already, the easiest thing is to collect them
in one directory, then use `scripts`:

    [files]
    scripts =
      bin/*

Alternatively, setuptools has a special way to directly invoke a Python
function from the command line, called the `console_scripts` entry
point. `pull-sp-sub` is an internal package that uses this:

    [entry_points]
    console_scripts =
      pull-sp-sub = pull_sp_sub:main

To explain that last line, it's *name-of-the-script* `=`
*dotted-path-of-the-python-module*`:`*name-of-the-python-function*. So
with this configuration, once the package is installed, setuptools
creates a script at `$VIRTUAL_ENV/bin/pull-sp-sub` which activates the
virtualenv and then calls the `main` function in the `pull_sp_sub`
module.

Scripts created this way are slightly slower to start up than scripts
that directly run a Python file. Also, setuptools seems to do more
dependency checking when starting a script like this, so if you
regularly live with broken dependencies inside your virtualenv, this
will be frustrating for you. On the other hand, scripts made this way
will work better on Windows, if that's one of your target environments.

### Including compiled shared libraries in both source and binary packages

This works because the NCBI Python/Linux environment is so homogeneous,
but it does cause problems - these compiled items are linux- and
architecture-specific, but this doesn't tell Python's packaging system
about that.  So for example if you run `pip install applog` on a Mac,
it will claim to succeed, but the library won't work.  See the next
section for how to do this in a more robust way.

This includes things that use the C++ Toolkit (see `python-applog` and
`cpp-toolkit-validators` for examples). These `.so` files should get
placed inside the python package hierarchy. Presumably, if you're
compiling them, they are build artifacts that won't be tracked by git,
so they won't be included automatically by `auto-package-data`. Instead,
once they are there, use `extra_files` to have the packaging system
notice them:

    [files]
    extra_files =
        ncbilog/libclog.so
        ncbilog/libclog.version

If your packages live inside a `src` directory, you do need to include
that in the `extra_files` path:

    [files]
    extra_files =
        src/mypkg/do_something_quickly.so

Notice that `extra_files` is different from `data_files` which we used
above.

### Including uncompiled C extensions (including Cython)

Packit can coexist with setuptools's support for C extensions. Here is
an [example with a C file that will be compiled on the user's
system](https://bitbucket.ncbi.nlm.nih.gov/projects/PY/repos/is_xml_encodable/browse/setup.py).
In that particular package, the author chose to require Cython for
developers but not for end users, so the distribution and the git repo
include both the `.pyx` file and the `.c` file it's translated to.

### Known Issues

  - If your Python package is not in the root of your Git repository (so
    `setup.py` is not in the same directory as `.git`), then
    `auto-package-data` will not work.
  - The `auto-package-data` section has configuration options, but they
    don't do anything right now
    ([PY-504](https://jira.ncbi.nlm.nih.gov/browse/PY-504)).

<a name="development"></a>
## Further Development

  - Add tests
  - Improve docs
  - More configuration options for existing facilities
  - New facilities
  - Allow extension through entry points

<!-- end list -->

1.  Unlike `source env/bin/activate`, this does not change the `$PATH`
    or set `$VIRTUAL_ENV`, so there are a few rare circumstances where
    it's not good enough: if your script needs to start another script
    using `subprocess` or `popen`, or if it tries to access data using a
    path relative to `$VIRTUAL_ENV`. Take a look at
    `env/bin/activate_this.py` if you encounter this problem.
