INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'social_django',
    'server',
    'party',
    'unrest.nopass',
    'unrest.user',
]

AUTH_USER_MODEL = 'user.User'
SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL
