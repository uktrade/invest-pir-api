# virtually admin.yp
from django.shortcuts import redirect

from investment_report.models import (
    PDFSection, Market, Sector, MarketLogo, SectorLogo
)

from django.apps import apps
from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin
from sorl.thumbnail.admin import AdminImageMixin
from modeltranslation.admin import TranslationAdmin


class InvestmentReportAdminSite(admin.AdminSite):
    site_header = 'Investment Report Generator'

    def get_app_list(self, request):
        """
        Order app list by the section attribute.
        """
        app_list = super().get_app_list(request)

        for app in app_list:
            for model in app['models']:
                model['order'] = getattr(
                    apps.get_model(app['app_label'], model['object_name']), 'SECTION', -1
                )

            app['models'].sort(key=lambda x: x['order'])

        return app_list

    def app_index(self, request, app_label, extra_context=None):
        """
        Hide the app index. Just duplicate functionality.
        """
        return redirect('reportadmin:index')

    def get_urls(self):
        from investment_report.views import admin_table, admin_table_detail
        from django.conf.urls import url

        urls = super(InvestmentReportAdminSite, self).get_urls()
        urls = [
            url(r'^validation-table/(?P<lang>[\w-]+)/(?P<market>[\w-]+)/(?P<sector>[\w-]+)/$',
                self.admin_view(admin_table_detail), name='validation_table_detail'),
            url(r'^validation-table/$', self.admin_view(admin_table), name='validation_table'),
        ] + urls
        return urls


admin_site = InvestmentReportAdminSite(name='reportadmin')


class PDFAdmin(MarkdownxModelAdmin, TranslationAdmin, admin.ModelAdmin):

    def has_add_permission(self, request):
        """
        Return a boolean to indicate whether `user` is permitted to create new
        instances of `self.model`
        """
        if self.model.SINGLETON:
            return self.model.objects.count() < 1
        else:
            return True


for klass in PDFSection.__subclasses__():
    """
    I can't be arrsed to create another 14 nearly identical classes

    Auto generate the admin for PDF section
    """
    Admin = type(
        '{}Admin'.format(klass),
        (PDFAdmin, ),
        {
            'model': klass,
            'menu_order': klass.SECTION,
        }
    )

    admin_site.register(klass, Admin)


class MarketAdmin(admin.ModelAdmin):
    pass


class SectorAdmin(admin.ModelAdmin):
    pass


class MarketLogoAdmin(AdminImageMixin, admin.ModelAdmin):
    pass


class SectorLogoAdmin(AdminImageMixin, admin.ModelAdmin):
    pass


admin_site.register(Market, MarketAdmin)
admin_site.register(Sector, SectorAdmin)
admin_site.register(MarketLogo, MarketLogoAdmin)
admin_site.register(SectorLogo, SectorLogoAdmin)
