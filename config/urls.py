from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls

from investment_report.admin import admin_site as investment_report_admin
from investment_report import views as investment_report_views

from markdownx import urls as markdownx

urlpatterns = i18n_patterns(
    url(r'^markdownx/', include(markdownx)),
    url(r'^django-admin/', include(admin.site.urls)),


    # PIR Stuff
    url(r'^investment-report-admin/', include(investment_report_admin.urls)),
    url(r'^investment-report/', include('investment_report.urls')),
    url(r'PIR/thankyou', investment_report_views.investment_report_download, name='pir_download'),
    url(r'PIR', investment_report_views.investment_report_form, name='pir'),


    url(r'^admin/', include(wagtailadmin_urls)),
    # url(r'^documents/', include(wagtaildocs_urls)),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),


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
