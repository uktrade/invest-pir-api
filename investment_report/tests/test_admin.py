from unittest.mock import Mock

import pytest
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User

from django.conf import settings

from moderation.constants import MODERATION_READY_STATE, \
    MODERATION_STATUS_APPROVED, MODERATION_STATUS_PENDING

from investment_report.admin import admin_site, PDFPreviewMixin, PDFAdmin
from investment_report.models import (
    UKGeographicOverview, Market, Sector,
    TalentAndEducationBySector, MacroContextBetweenCountries
)


class AdminTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='admin', email='admin@example.com',
            is_superuser=True, is_staff=True,
            password='top_secret')

    def test_app_list_order(self):
        request = self.factory.get(reverse('reportadmin:index'))
        request.user = self.user
        app_list = admin_site.get_app_list(request)

        for app in app_list:
            if app['app_label'] == 'investment_report':
                break

        for model in app['models']:
            if model['object_name'] == 'UKGeographicOverview':
                break

        self.assertEquals(model['order'], UKGeographicOverview.SECTION)

        for model in app['models']:
            if model['object_name'] == 'Market':
                break

        self.assertEquals(model['order'], -1)

    def test_pdf_links(self):
        market = Market.objects.create(name='market')
        Sector.objects.create(name='other')
        sector = Sector.objects.create(name='actual')
        talent = TalentAndEducationBySector.objects.create(
            content_en='test', sector=sector
        )

        mixin = PDFPreviewMixin()

        # In an initial state, there should be no live object,
        # only a preview link
        preview = mixin.get_pdf_links(talent.moderated_object)
        self.assertEquals(
            preview,
            # and the sector or market is controled by the sector
            # of the model being previewed
            {'preview': '/investment-report/preview/en/market/actual/pdf'}
        )

        talent.moderated_object.state = MODERATION_READY_STATE
        talent.moderated_object.status = MODERATION_STATUS_APPROVED
        talent.moderated_object.save()

        live = mixin.get_pdf_links(talent.moderated_object)
        self.assertEquals(
            live,
            # and the sector or market is controled by the sector
            # of the model being previewed
            {'live': '/investment-report/current/en/market/actual/pdf'}
        )

        talent.moderated_object.status = MODERATION_STATUS_PENDING
        talent.moderated_object.save()

        live_and_preview = mixin.get_pdf_links(talent.moderated_object)
        self.assertEquals(
            live_and_preview,
            {
                'preview': '/investment-report/preview/en/market/actual/pdf',
                'live': '/investment-report/current/en/market/actual/pdf'
            }
        )

        # Test same thing but have url dictated by market
        market = Market.objects.create(name='china')
        macro_context = MacroContextBetweenCountries.objects.create(
            content_en='test', market=market
        )

        preview = mixin.get_pdf_links(macro_context.moderated_object)
        self.assertEquals(
            preview,
            # and the sector or market is controled by the sector
            # of the model being previewed
            {'preview': '/investment-report/preview/en/china/other/pdf'}
        )

    @pytest.mark.xfail
    def test_pdf_admin_change_view_for_preview_links(self):
        Market.objects.create(name='market')
        sector = Sector.objects.create(name='actual')
        talent = TalentAndEducationBySector.objects.create(
            content_en='test', sector=sector
        )

        request = self.factory.get(reverse('reportadmin:index'))
        request.user = self.user
        request._messages = Mock()

        response = PDFAdmin(TalentAndEducationBySector,
                            admin_site).change_view(request, str(talent.id))

        self.assertEquals(len(response.context_data['preview']),
                          len(settings.LANGUAGES))
