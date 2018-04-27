# virtually admin.yp
from django.shortcuts import redirect

from investment_report.models import (
    PDFSection, Market, Sector, MarketLogo, SectorLogo, SectorOverview
)

from django.apps import apps
from django.contrib import admin
from django.db import models
from django.contrib import admin

from moderation.admin import ModerationAdmin, ModeratedObjectAdmin
from moderation.models import ModeratedObject
from moderation.helpers import automoderate

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


class PDFAdmin(MarkdownxModelAdmin, TranslationAdmin, ModerationAdmin, admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        # This is because django-model translations monkey patches
        # the base manager object causing the base manager to inherit
        # from a user defined manager.

        # This breaks object saving because when determining to do
        # an INSERT or an UPDATE, it does a test to see if the object
        # is in the _base_manager queryset. In our case it won't be if:
        # 
        # The object hasn't been approved yet as the _base_manager query
        # will be searching for an object that's in a published state
        # 
        # Sorry to all that have read this. 1 day deadlines and coubled
        # together django solutions are sometimes a bit awful.
        #
        # [Vomits]
        #
        #               %%%%%%
        #              %%%% = =
        #              %%C    >
        #               _)' _( .' ,
        #            __/ |_/\   " *. o
        #           /` \_\ \/     %`= '_  .
        #          /  )   \/|      .^',*. ,
        #         /' /-   o/       - " % '_
        #        /\_/     <       = , ^ ~ .
        #        )_o|----'|          .`  '
        #    ___// (_  - (\
        #   ///-(    \'   \\ b'ger
        obj.__class__._base_manager.__class__ = models.Manager

        obj.save()
        automoderate(obj, request.user)


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

admin.site.unregister(ModeratedObject)
admin_site.register(ModeratedObject, ModeratedObjectAdmin)
