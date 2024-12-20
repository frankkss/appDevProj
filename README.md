# appDevProj


### Change to python 3.10.12 using pyenv

```
# Check current version
$ python --version
```

```
# install pyenv
$ curl https://pyenv.run | bash
```

```
# update shell configuration
$ export PATH="$HOME/.pyenv/bin:$PATH"
$ eval "$(pyenv init --path)"
$ eval "$(pyenv init -)"
$ eval "$(pyenv virtualenv-init -)"
```

```
# Restart shell
$ exec "$SHELL"
```

```
# Install py 3.10.12
$ pyenv install 3.10.12

# set to global variable
$ pyenv global 3.10.12

# check version if successfully changed
$ python --version
```

```
$ set FLASK_APP=app.py
```

```
$ flask run
```
