# NO DEBUG for production!
DEBUG = False

# Email me if something breaks.
ADMINS = (
    ('Kevin Williams', 'kevin@weblivion.com'),
)

# Email settings
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = "isolationism"
EMAIL_HOST_PASSWORD = "autechre"
DEFAULT_FROM_EMAIL = 'noreply@weblivion.com'
SERVER_EMAIL = 'noreply@weblivion.com'

# Reply-to MUST come from an account registered to the user!
EMAIL_NOTIFICATION_LIST = (
    "kevin@weblivion.com",
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'stabbing_django',
        'USER': 'csoweb',
        'PASSWORD': 'Auagf998fGN',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Use memcached back-end if available
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:23380',
        'TIMEOUT': 480,
    }
}

# Prevent DOS attacks
CACHE_MIDDLEWARE_KEY_PREFIX = "stabbing"
CACHE_MIDDLEWARE_SECONDS = 60

ALLOWED_HOSTS = [
    'dayswithnostabbings.ca',
    'www.dayswithnostabbings.ca',
    'ottawa.dayswithnostabbings.ca',
]

# This value should be different in production for faster delivery.
STATIC_ROOT = '/home/isolationism/webapps/stabbing_media/static'
STATIC_URL = '/static/'
