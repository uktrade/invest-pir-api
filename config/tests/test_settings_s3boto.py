import os
import pytest


aws_enabled = pytest.mark.skipif(
    os.getenv('AWS_ACCESS_KEY_ID') != 'true',
    reason="aws toolbar disabled")

aws_disabled = pytest.mark.skipif(
    os.getenv('AWS_ACCESS_KEY_ID') == 'true',
    reason="aws toolbar enabled")


@aws_enabled
def test_s3_domain_present(settings):
    assert settings.AWS_S3_CUSTOM_DOMAIN is not None


@aws_disabled
def test_s3_storage_backend_absent(settings):
    assert settings.DEFAULT_FILE_STORAGE != \
           'storages.backends.s3boto3.S3Boto3Storage'


@aws_enabled
def test_s3_storage_backend_present(settings):
    assert settings.DEFAULT_FILE_STORAGE == \
           'storages.backends.s3boto3.S3Boto3Storage'


@aws_enabled
def test_s3_media_url(settings):
    assert settings.AWS_S3_CUSTOM_DOMAIN in settings.MEDIA_URL
