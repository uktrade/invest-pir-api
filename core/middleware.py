import logging
import sigauth.middleware

from django.conf import settings
from django.http import HttpResponse
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


def AdminIpRestrictionMiddleware(get_response):

    def middleware(request):
        if resolve(request.path).app_name == 'admin':
            if settings.RESTRICT_ADMIN:
                try:
                    remote_address = request.headers['x-forwarded-for'].split(',')[-2].strip()  # noqa: E501
                except (IndexError, KeyError):
                    logger.warning(
                        'X-Forwarded-For header is missing or does not '
                        'contain enough elements to determine the '
                        'client\'s ip')
                    return HttpResponse('Unauthorized', status=401)

                if remote_address not in settings.ALLOWED_ADMIN_IPS:
                    return HttpResponse('Unauthorized', status=401)

        return get_response(request)

    return middleware


class AdminPermissionCheckMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwarg):
        if request.user is not None:
            if request.resolver_match.namespace == 'admin' or request.path_info.startswith('/admin/login'):
                if not request.user.is_staff and request.user.is_authenticated:
                    return HttpResponse('User not authorized for admin access', status=401)


class SignatureCheckMiddleware(
    sigauth.middleware.SignatureCheckMiddlewareBase
):
    secret = settings.SIGNATURE_SECRET

    def should_check(self, request):
        if request.resolver_match.namespace in [
            'admin', 'healthcheck', 'authbroker_client'
        ] or request.path_info.startswith('/admin/login'):
            return False
        return super().should_check(request)
