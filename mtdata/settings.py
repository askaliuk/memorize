"""
Contains the database access settings.
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mtdata.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    }
}

INSTALLED_APPS = (
    'app',
)
