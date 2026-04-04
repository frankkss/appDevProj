# Reliamed App 

```
This project is a web application named "Reliamed" designed to manage pharmaceuticals and user profiles. 
It includes features for user registration, login, profile management, product purchase and sale, and image classification for medicine identification. 
The application is built using Flask, a lightweight web framework for Python, and integrates a machine learning model for image classification.
```


```
$ git clone https://github.com/frankkss/appDevProj
```

### Change to python 3.10.12 using pyenv

```
# Check current version
$ python --version
```

```
# install pyenv
$ curl https://pyenv.run | bash
```

### if you encunter error like thissssss; "WARNING: Can not proceed with installation. Kindly remove the '/root/.pyenv' directory first."
### try to remove firt the root pyenv using this command "rm -rf /root/.pyenv"
### then try to install again pyenv

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
$ pip install -r requirements.txt
```

```
$ set FLASK_APP=app.py
```

```
$ flask run
```

## Default Admin Credentials

After setting up the database, use these credentials to access the admin panel:

- **Admin URL:** `http://localhost:5000/admin-login`
- **Username:** `admin`
- **Password:** `admin123`

⚠️ **Important:** Change the default password after first login for security.

## Features

- User registration and authentication
- Profile management with image upload
- Medicine marketplace
- ML-powered medicine classification
- Admin panel for user and medicine management
- Google OAuth integration

