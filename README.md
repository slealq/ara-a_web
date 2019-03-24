# oddcrawler
This project is developed as part of a community service for TCU 677 of the
Universidad de Costa Rica.

# Dependencies
This webcrawler will run on **Firefox**. Your system needs to have a running
installation of firefox to be run. Before you can use
`oddwebcrawler.webpage_extractors` you will need to get `geckodriver`. This can
be achieved by downloading it from
[mozilla's github](https://github.com/mozilla/geckodriver/releases) itself, or
from your system's sources if it is supported:

For archlinux you can do:
```ssh
$ sudo pacman -S geckodriver
```

There are some other dependencies from pypi repos:

1. selenium

But you **should not** worry about them, since installing the package resolves
this dependencies.

# Installation
You might want to set up an environment first. For this it is recommended to
use [pyenv](https://github.com/pyenv/pyenv). Please follow it's installation
instructions.

Once you have `pyenv`, you can do the following:

```sh
$ pyenv install 3.7.2
$ pyenv global 3.7.2
```

You can confirm that now you are in an environment running:

```sh
$ which python
```

This should point to `/home/$USER/.pyenv/shims/python`

Now clone this repo:

```sh
$ git clone https://github.com/slealq/oddcrawler
$ pip install .
```

Install package with a symlink, so that changes to the source
files will be inmediately available to the users of the package, as specified in
[python-packaging](https://python-packaging.readthedocs.io/en/latest/minimal.html).

```sh
$ pip install -e .
```

Now you can import `oddwebcrawler` in any python inside this environment.

# Development
For development, important to consider:

1. **Follow PEP8 guidelines:** If you are on linux you can always check if
there's a violation of some rule, by using `flake8`.

2. **English for variables and comments:** Try to avoid using other languages
in development of code.

3. **Create tests for functions:** When testing code, try to write a script for
testing that function. It might be useful for others.

4. **Documentation:** Document class definitions, methods and functions to
ease collaboration. Be clear in your documentation.
