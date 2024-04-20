DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

EXTERNAL_APPS = [
    "rest_framework",
    "corsheaders",
    "django_extensions",
]

LOCAL_APPS = [
    "auth.users",
    "standards",
]

INSTALLED_APPS = [
    *DJANGO_APPS,
    *EXTERNAL_APPS,
    *LOCAL_APPS,
]
