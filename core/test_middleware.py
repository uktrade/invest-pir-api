import pytest
from django.http import HttpResponse

from .middleware import AdminIpRestrictionMiddleware

from core.test_views import reload_urlconf
from django.urls import reverse


def test_ip_restriction_middleware_is_enabled(client, settings):
    settings.RESTRICT_ADMIN = True
    assert client.get('/admin/').status_code == 401


def test_ip_restriction_applies_to_admin_only(rf, settings):
    settings.RESTRICT_ADMIN = True

    request = rf.get('/api/pir/')

    assert AdminIpRestrictionMiddleware(lambda _: HttpResponse(status=200))(request).status_code == 200  # noqa


def test_ip_restriction_enabled_false(rf, settings):
    settings.RESTRICT_ADMIN = False

    request = rf.get('/admin/', HTTP_X_FORWARDED_FOR='')

    assert AdminIpRestrictionMiddleware(lambda _: HttpResponse(status=200))(request).status_code == 200  # noqa


def test_ip_restriction_missing_x_forwarded_header(rf, settings):
    settings.RESTRICT_ADMIN = True

    request = rf.get('/admin/', HTTP_X_FORWARDED_FOR='1.1.1.1')

    assert AdminIpRestrictionMiddleware(lambda _: HttpResponse(status=200))(request).status_code == 401  # noqa


def test_ip_restriction_invalid_x_forwarded_header(rf, settings):
    settings.RESTRICT_ADMIN = True

    request = rf.get('/admin/', HTTP_X_FORWARDED_FOR='1.1.1.1')

    assert AdminIpRestrictionMiddleware(lambda _: HttpResponse(status=200))(request).status_code == 401  # noqa


def test_ip_restriction_valid_ip(rf, settings):
    settings.RESTRICT_ADMIN = True
    settings.ALLOWED_ADMIN_IPS = ['2.2.2.2']

    request = rf.get('/admin/',
                     HTTP_X_FORWARDED_FOR='1.1.1.1, 2.2.2.2, 3.3.3.3')

    assert AdminIpRestrictionMiddleware(lambda _: HttpResponse(status=200))(request).status_code == 200  # noqa


def test_ip_restriction_invalid_ip(rf, settings):
    settings.RESTRICT_ADMIN = True
    settings.ALLOWED_ADMIN_IPS = ['1.1.1.1']

    request = rf.get('/admin/',
                     HTTP_X_FORWARDED_FOR='1.1.1.1, 2.2.2.2, 3.3.3.3')

    assert AdminIpRestrictionMiddleware(lambda _: HttpResponse(status=200))(request).status_code == 401  # noqa

    settings.ALLOWED_ADMIN_IPS = ['3.3.3.3']

    assert AdminIpRestrictionMiddleware(lambda _: HttpResponse(status=200))(request).status_code == 401  # noqa


SIGNATURE_CHECK_REQUIRED_MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'core.middleware.SignatureCheckMiddleware',
    'core.middleware.AdminPermissionCheckMiddleware',
]


def test_signature_check_middleware_admin(admin_client, settings):
    settings.MIDDLEWARE_CLASSES = SIGNATURE_CHECK_REQUIRED_MIDDLEWARE_CLASSES
    settings.FEATURE_ENFORCE_STAFF_SSO_ENABLED = True
    reload_urlconf()

    response = admin_client.get(reverse('admin:auth_user_changelist'))

    assert response.status_code == 200


def test_signature_check_middleware_admin_login(admin_client, settings):
    settings.MIDDLEWARE_CLASSES = SIGNATURE_CHECK_REQUIRED_MIDDLEWARE_CLASSES
    settings.FEATURE_ENFORCE_STAFF_SSO_ENABLED = True
    reload_urlconf()
    response = admin_client.get(reverse('admin:login'))

    assert response.status_code == 302


def test_signature_check_middleware_authbroker_login(admin_client, settings, admin_user):
    settings.MIDDLEWARE_CLASSES = SIGNATURE_CHECK_REQUIRED_MIDDLEWARE_CLASSES
    settings.FEATURE_ENFORCE_STAFF_SSO_ENABLED = True
    reload_urlconf()
    admin_client.force_login(admin_user)

    response = admin_client.get(reverse('authbroker_client:login'))

    assert response.status_code == 302


@pytest.mark.django_db
def test_authenticated_user_middleware_no_user(client, settings):
    settings.MIDDLEWARE_CLASSES = SIGNATURE_CHECK_REQUIRED_MIDDLEWARE_CLASSES
    settings.FEATURE_ENFORCE_STAFF_SSO_ENABLED = True
    reload_urlconf()
    response = client.get(reverse('admin:login'))

    assert response.status_code == 302
    assert response.url == reverse('authbroker_client:login')


@pytest.mark.django_db
def test_authenticated_user_middleware_authorised_no_staff(client, settings, admin_user):
    settings.MIDDLEWARE_CLASSES = SIGNATURE_CHECK_REQUIRED_MIDDLEWARE_CLASSES
    settings.FEATURE_ENFORCE_STAFF_SSO_ENABLED = True
    reload_urlconf()
    client.force_login(admin_user)

    response = client.get(reverse('admin:login'))

    assert response.status_code == 302


@pytest.mark.django_db
def test_authenticated_user_middleware_authorised_with_staff(client, settings, admin_user):
    settings.MIDDLEWARE_CLASSES = SIGNATURE_CHECK_REQUIRED_MIDDLEWARE_CLASSES
    settings.FEATURE_ENFORCE_STAFF_SSO_ENABLED = True
    reload_urlconf()
    admin_user.is_staff = True
    admin_user.save()
    client.force_login(admin_user)
    response = client.get(reverse('admin:login'))

    assert response.status_code == 302
