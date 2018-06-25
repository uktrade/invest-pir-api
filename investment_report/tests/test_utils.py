from django.test import TestCase
from django.utils import translation


# Importing this one as this is a simple model without sector
# or market
from investment_report.models import UKGeographicOverview
from investment_report.utils import filter_translations_and_moderation


class FiltersModerationTranslationTestCase(TestCase):

    def test_moderation_filtering(self):
        geographic_overview = UKGeographicOverview.objects.create(
            content_en='English',
            content_es='Spanish'
        )

        self.assertEquals(
            UKGeographicOverview.objects.count(), 0
        )

        self.assertEquals(
            UKGeographicOverview.unmoderated_objects.count(), 1
        )

        self.assertIsNotNone(
            filter_translations_and_moderation(UKGeographicOverview,
                                               moderated=False)
        )

        # Test object not registered with moderation
        geographic_overview.moderated_object.delete()
        self.assertIsNotNone(
            filter_translations_and_moderation(UKGeographicOverview,
                                               moderated=False)
        )

    def test_basic_language_filtering(self):
        UKGeographicOverview.objects.create(
            content_en='English',
            content_es='Spanish'
        )

        # Test with english
        moderated = filter_translations_and_moderation(UKGeographicOverview)
        unmoderated = filter_translations_and_moderation(
            UKGeographicOverview, moderated=False
        )
        self.assertIsNone(moderated)
        self.assertIsNotNone(unmoderated)

        # Test with spanish
        with translation.override('es'):
            moderated = filter_translations_and_moderation(
                UKGeographicOverview)

            unmoderated = filter_translations_and_moderation(
                UKGeographicOverview, moderated=False
            )
            self.assertIsNone(moderated)
            self.assertIsNotNone(unmoderated)

        # Test with non-existant language
        with translation.override('pt'):
            moderated = filter_translations_and_moderation(
                UKGeographicOverview)

            unmoderated = filter_translations_and_moderation(
                UKGeographicOverview, moderated=False
            )

            self.assertIsNone(moderated)
            self.assertIsNone(unmoderated)
