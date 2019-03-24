# oddcrawler
This project is developed as part of a community service for TCU 677 of the
Universidad de Costa Rica.

# Dependencies
This webcrawler will run on **Firefox**. Your system needs to have a running
installation of firefox to be run. Before you can use
`oddwebcrawler.webpage_extractors` you will need to get [geckodriver](https://github.com/mozilla/geckodriver) in conjunction with [selenium](https://github.com/SeleniumHQ/selenium).

For Arch Linux all you need to do is:
```ssh
$ sudo pacman -S geckodriver
```
For Ubuntu the process is a bit longer:
1. **Download and install geckodriver.**
   
   ```ssh
   $ wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
   $ tar -xvzf geckodriver*
   $ sudo chmod +x geckodriver
   $ sudo cp geckodriver /usr/local/bin/
   ```

2. **Download and install Selenium Python bindings.** 

    ```sh
    $ sudo apt-get install python-pip
    $ sudo pip install selenium
    ```
# Installation
You might want to set up an environment first. For this it is recommended to
use [pyenv](https://github.com/pyenv/pyenv). Installation instructions for it are shown below:

1. **Check out pyenv where you want it installed.**
   A good place to choose is `$HOME/.pyenv` (but you can install it somewhere else).

        $ git clone https://github.com/pyenv/pyenv.git ~/.pyenv


2. **Define environment variable `PYENV_ROOT`** to point to the path where
   pyenv repo is cloned and add `$PYENV_ROOT/bin` to your `$PATH` for access
   to the `pyenv` command-line utility.

    ```sh
    $ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
    $ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
    ```
    - **Zsh note**: Modify your `~/.zshenv` file instead of `~/.bash_profile`.
    - **Ubuntu and Fedora note**: Modify your `~/.bashrc` file instead of `~/.bash_profile`.
    - **Proxy note**: If you use a proxy, export `http_proxy` and `HTTPS_PROXY` too.

3. **Add `pyenv init` to your shell** to enable shims and autocompletion.
   Please make sure `eval "$(pyenv init -)"` is placed toward the end of the shell
   configuration file since it manipulates `PATH` during the initialization.
    ```sh
    $ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
    ```
    - **Zsh note**: Modify your `~/.zshenv` file instead of `~/.bash_profile`.
    - **fish note**: Use `pyenv init - | source` instead of `eval (pyenv init -)`.
    - **Ubuntu and Fedora note**: Modify your `~/.bashrc` file instead of `~/.bash_profile`.

    **General warning**: There are some systems where the `BASH_ENV` variable is configured
    to point to `.bashrc`. On such systems you should almost certainly put the abovementioned line
    `eval "$(pyenv init -)"` into `.bash_profile`, and **not** into `.bashrc`. Otherwise you
    may observe strange behaviour, such as `pyenv` getting into an infinite loop.
    See [#264](https://github.com/pyenv/pyenv/issues/264) for details.

4. **Restart your shell so the path changes take effect.**
   You can now begin using pyenv.
    ```sh
    $ exec "$SHELL"
    ```

5. **Install Python build dependencies** before attempting to install a new Python version.  The
   [pyenv wiki](https://github.com/pyenv/pyenv/wiki) provides suggested installation packages
   and commands for various operating systems.
   
6. **Install Python into `$(pyenv root)/versions`.**
   For example, to download and install Python 3.7.2, run:
    ```sh
    $ pyenv install 3.7.2
    $ pyenv global 3.7.2
    ```
    
After the [pyenv](https://github.com/pyenv/pyenv) installation is complete, you can confirm that now you are in an environment running:

```sh
$ which python
```

This should point to `/home/$USER/.pyenv/shims/python`

Now clone this repo:

```sh
$ git clone https://github.com/slealq/oddcrawler
```

Inside the repo's folder, install package with a symlink, so that changes to the source
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
