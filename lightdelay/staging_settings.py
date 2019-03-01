from lightdelay.dev_settings import *

SECRET_KEY = '1234asdfqwersdfhgbw5fvufwh4euuaew3478gqc'
DEBUG = False
ALLOWED_HOSTS = [
    'xve20vgtn4.execute-api.us-west-2.amazonaws.com',
    'staging.lightdelay.to',
]

AWS_S3_BUCKET_NAME_STATIC = "staging.static.lightdelay.to"
AWS_S3_PUBLIC_URL_STATIC = "https://staging.static.lightdelay.to/"
