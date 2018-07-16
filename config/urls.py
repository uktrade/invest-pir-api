from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import auth

from investment_report.admin import admin_site as investment_report_admin
from investment_report.views import api
from investment_report.views.auth import ResetRequestView


from markdownx import urls as markdownx

urlpatterns = i18n_patterns(
    url(r'^markdownx/', include(markdownx)),
    # PIR Stuff
    url(r'^admin/', include(investment_report_admin.urls)),

    url(r'^admin/password_reset/$',
        auth.views.password_reset,
        name='admin_password_reset'),

    url(r'^admin/password_reset/done/$',
        auth.views.password_reset_done,
        name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth.views.password_reset_confirm,
        name='password_reset_confirm'),

    url(r'^reset/done/$',
        auth.views.password_reset_complete,
        name='password_reset_complete'),


    url(r'^unlock-account', ResetRequestView.as_view(), name='reset_request'),

    url(r'^investment-report/', include('investment_report.urls')),

    url(r'^api/pir/$', api.PIRAPI.as_view(), name='pir_api'),
    url(r'^api/pir/(?P<identifier>\d+)/$',
        api.PIRAPI.as_view(), name='pir_api_detail'),

    prefix_default_language=False)


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if settings.ENABLE_DEBUG_TOOLBAR:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
