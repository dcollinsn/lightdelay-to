from lightdelay.local_settings import *

APPEND_SLASH = False

ALLOWED_HOSTS = [
    'itkucjh4u8.execute-api.us-west-2.amazonaws.com',
    'dev.lightdelay.to',
]

INSTALLED_APPS = INSTALLED_APPS + [
    'django_s3_storage',
]

STATIC_ROOT = '/tmp/static'
SASS_PROCESSOR_ROOT = '/tmp/static'

STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
AWS_S3_BUCKET_NAME_STATIC = "dev.static.lightdelay.to"
AWS_S3_PUBLIC_URL_STATIC = "https://dev.static.lightdelay.to/"
