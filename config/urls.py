from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import path
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.contrib.auth.decorators import login_required

from investment_report.admin import admin_site as investment_report_admin
from investment_report.views import api
from investment_report.views.auth import ResetRequestView


from markdownx import urls as markdownx

urlpatterns = i18n_patterns(
    path('markdownx/', include(markdownx)),
    path(
        'admin/password_reset/',
        PasswordResetView.as_view(),
        name='admin_password_reset',
    ),
    path(
        'admin/password_reset/done/',
        PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    re_path(
        r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    re_path(r'^unlock-account', ResetRequestView.as_view(), name='reset_request'),
    path('investment-report/', include('investment_report.urls')),
    path('api/pir/', api.PIRAPI.as_view(), name='pir_api'),
    path(
        'api/pir/<int:identifier>/', api.PIRAPI.as_view(), name='pir_api_detail'
    ),
    # PIR Stuff
    path('admin/', investment_report_admin.urls),
    prefix_default_language=False,
)

if settings.FEATURE_ENFORCE_STAFF_SSO_ENABLED:
    authbroker_urls = [
        path(
            'admin/login/',
            RedirectView.as_view(
                url=reverse_lazy('authbroker_client:login'),
                query_string=True,
            ),
        ),
        path('auth/', include('authbroker_client.urls')),
    ]

    urlpatterns = [path('', include(authbroker_urls))] + urlpatterns

if settings.FEATURE_PIR_OPENAPI_ENABLED:
    urlpatterns += [
        path('openapi/', SpectacularAPIView.as_view(), name='schema'),
        path(
            'openapi/ui/',
            login_required(
                SpectacularSwaggerView.as_view(url_name='schema'),
                login_url='admin:login',
            ),
            name='swagger-ui',
        ),
        path(
            'openapi/ui/redoc/',
            login_required(
                SpectacularRedocView.as_view(url_name='schema'), login_url='admin:login'
            ),
            name='redoc',
        ),
    ]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if settings.ENABLE_DEBUG_TOOLBAR:
        import debug_toolbar

        urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
