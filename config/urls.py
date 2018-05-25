from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from investment_report.admin import admin_site as investment_report_admin
from investment_report.views import api


from markdownx import urls as markdownx

urlpatterns = i18n_patterns(
    url(r'^markdownx/', include(markdownx)),
    # PIR Stuff
    url(r'^admin/', include(investment_report_admin.urls)),
    url(r'^api/pir/', api.PIRAPI.as_view(), name='pir_api'),
    url(r'^investment-report/', include('investment_report.urls')),

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
