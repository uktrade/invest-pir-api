from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


def StaticRootS3BotoStorage(): return S3Boto3Storage(location='static')


def MediaRootS3BotoStorage(): return S3Boto3Storage(location='media')


class PDFS3Boto3Storage(S3Boto3Storage):
    access_key = settings.AWS_S3_PDF_STORE_ACCESS_KEY_ID
    secret_key = settings.AWS_S3_PDF_STORE_SECRET_ACCESS_KEY
    bucket_name = settings.AWS_S3_PDF_STORE_BUCKET_NAME
    region_name = settings.AWS_S3_PDF_STORE_BUCKET_REGION
    custom_domain = None
