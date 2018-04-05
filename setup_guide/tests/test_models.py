from wagtail.tests.utils import WagtailPageTests
from setup_guide.models import SetupGuideLandingPage, SetupGuidePage
from home.models import HomePage


class SetupGuideLandingPageTests(WagtailPageTests):
    def test_can_create_under_homepage(self):
        self.assertCanCreateAt(HomePage, SetupGuideLandingPage)

    def test_setup_guide_page_subpages(self):
        # A SetupGuidePage can only have other SetupGuidePage children
        self.assertAllowedSubpageTypes(
            SetupGuideLandingPage, {SetupGuidePage})


class SetupGuidePageTests(WagtailPageTests):
    def test_can_create_under_landing_page(self):
        self.assertCanCreateAt(SetupGuideLandingPage, SetupGuidePage)
