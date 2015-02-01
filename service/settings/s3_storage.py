import os

MEDIA_ROOT = '/media/' 
STATIC_ROOT = '/static/'

# Amazon S3 credentials
AWS_ACCESS_KEY_ID       = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY   = os.environ.get('AWS_SECRET_ACCESS_KEY', '')

# Amazon S3 URL
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", '')
S3_URL = 'http://%s.s3-website-eu-west-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Static files location
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATIC_URL = S3_URL + STATIC_ROOT

# Default File storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
MEDIA_URL = S3_URL + MEDIA_ROOT
