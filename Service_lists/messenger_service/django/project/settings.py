# settings.py

INSTALLED_APPS = [
    ...
    'channels',
    ...
]

ASGI_APPLICATION = "project.asgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'messenger',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('redis', 6379)],
        },
    },
}
