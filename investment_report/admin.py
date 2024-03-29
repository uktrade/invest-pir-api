# virtually admin.yp

from investment_report.models import (
    PDFSection, Market, Sector, PIRRequest, MarketContact
)

import django
from django.urls import reverse
from django.apps import apps
from django.db import models
from django.contrib import admin
from django.contrib.sites.models import Site
from django.conf import settings

from moderation.admin import ModerationAdmin, ModeratedObjectAdmin
from moderation.models import ModeratedObject
from moderation.helpers import automoderate
from moderation import moderation
from moderation.diff import get_changes_between_models
from moderation.constants import MODERATION_READY_STATE, \
    MODERATION_STATUS_APPROVED

# Annoying that I have to import this as I've overloaded the admin
from axes.admin import AccessLogAdmin
from axes.models import AccessLog

from django.contrib.contenttypes.models import ContentType
from markdownx.admin import MarkdownxModelAdmin
from modeltranslation.admin import TranslationAdmin
from django.contrib.auth.admin import (
    User, Group, UserAdmin, GroupAdmin
)


def _get_pdf_args(obj):
    _market = Market.objects.first()
    _sector = Sector.objects.first()

    if hasattr(obj, 'market'):
        _market = obj.market

    if hasattr(obj, 'sector'):
        _sector = obj.sector

    return (_market.name, _sector.name)


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
                    apps.get_model(
                        app['app_label'], model['object_name']), 'SECTION', -1)

            app['models'].sort(key=lambda x: x['order'])

        return app_list


admin_site = InvestmentReportAdminSite(name='reportadmin')


class PDFPreviewMixin:

    def get_pdf_links(self, moderated_object):
        changed_object = None
        live_object = None

        # if the moderation object is not approved there will be a changed
        # object
        if moderated_object.status != MODERATION_STATUS_APPROVED:
            changed_object = moderated_object.changed_object

            # In a ready state there will be a live object too
            if moderated_object.state == MODERATION_READY_STATE:
                live_object = moderated_object.content_object
        # If it's already been approved there will just be a live object
        else:
            live_object = moderated_object.content_object

        res = {}

        if changed_object:
            res['preview'] = reverse(
                'preview_investment_report_pdf', args=(
                    'en', *_get_pdf_args(changed_object)))

        if live_object:
            res['live'] = reverse(
                'investment_report_pdf', args=(
                    'en', *_get_pdf_args(live_object)))

        return res


class PDFAdmin(
    MarkdownxModelAdmin,
    TranslationAdmin,
    ModerationAdmin,
    admin.ModelAdmin,
    PDFPreviewMixin
):
    change_form_template = "admin/pdf_changeform.html"

    def change_view(self, request, object_id, extra_context={}):
        model = self.model.unmoderated_objects.get(id=object_id)

        preview_links = []

        for lang in settings.LANGUAGES:
            link = (
                'Preview PDF {}'.format(lang[0]),
                reverse(
                    'preview_investment_report_pdf', args=(
                        lang[0], *_get_pdf_args(model)
                    ))
            )
            preview_links.append(link)

        return super().change_view(
            request,
            object_id,
            extra_context={
                'preview': preview_links
            })

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

        obj.__class__._base_manager.__class__ = models.Manager

        obj.save()
        automoderate(obj, request.user)


for klass in PDFSection.__subclasses__():
    """
    Auto generate the admin for PDF section
    """
    Admin = type(
        '{}Admin'.format(klass),
        (PDFAdmin,),
        {
            'model': klass,
            'menu_order': klass.SECTION,
        }
    )

    admin_site.register(klass, Admin)


@admin.register(PIRRequest, site=admin_site)
class PIRRequestAdmin(admin.ModelAdmin):
    change_list_template = "admin/pir_request_list.html"
    list_display = [f.name for f in PIRRequest._meta.fields]
    list_filter = ('market', 'sector', 'gdpr_optin')


@admin.register(Market, site=admin_site)
class MarketAdmin(admin.ModelAdmin):
    pass


@admin.register(Sector, site=admin_site)
class SectorAdmin(admin.ModelAdmin):
    pass


@admin.register(MarketContact, site=admin_site)
class MarketContactAdmin(admin.ModelAdmin):
    pass


@admin.register(ModeratedObject, site=admin_site)
class CustomModeratedObjectAdmin(ModeratedObjectAdmin, PDFPreviewMixin):
    change_form_template = 'admin/moderate_object.html'

    def change_view(self, request, object_id, extra_context=None):
        """
        Copied and pasted from the base class as I needed to override
        extra_context

        And the class hasn't been sublclassed properly to allow that.
        """
        moderated_object = ModeratedObject.objects.get(pk=object_id)

        changed_obj = moderated_object.changed_object

        moderator = moderation.get_moderator(changed_obj.__class__)

        if moderator.visible_until_rejected:
            old_object = changed_obj
            new_object = moderated_object.get_object_for_this_type()
        else:
            old_object = moderated_object.get_object_for_this_type()
            new_object = changed_obj

        changes = list(get_changes_between_models(
            old_object,
            new_object,
            moderator.fields_exclude,
            resolve_foreignkeys=moderator.resolve_foreignkeys).values())

        if request.POST:
            admin_form = self.get_form(request, moderated_object)(request.POST)

            if admin_form.is_valid():
                reason = admin_form.cleaned_data['reason']
                if 'approve' in request.POST:
                    moderated_object.approve(request.user, reason)
                elif 'reject' in request.POST:
                    moderated_object.reject(request.user, reason)

        content_type = ContentType.objects.get_for_model(changed_obj.__class__)
        try:
            object_admin_url = reverse("admin:%s_%s_change" %
                                       (content_type.app_label,
                                        content_type.model),
                                       args=(changed_obj.pk,))
        except reverse.NoReverseMatch:
            object_admin_url = None

        # This is the only bit of code overridden.
        try:
            preview_links = self.get_pdf_links(moderated_object)
        except BaseException:
            preview_links = None

        extra_context = {
            'changes': changes,
            'django_version': django.get_version()[:3],
            'object_admin_url': object_admin_url,
            # This is the only bit of code overridden
            'preview': preview_links
        }

        return super(ModeratedObjectAdmin, self).change_view(
            request,
            object_id,
            extra_context=extra_context)


admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(Site, admin.ModelAdmin)
admin_site.register(AccessLog, AccessLogAdmin)

admin.site.unregister(ModeratedObject)
admin.site.unregister(AccessLog)
