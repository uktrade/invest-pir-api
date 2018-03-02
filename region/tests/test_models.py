from wagtail.tests.utils import WagtailPageTests
from region.models import RegionLandingPage, RegionPage
from home.models import HomePage


class RegionLandingPageTests(WagtailPageTests):
    def test_can_create_under_homepage(self):
        self.assertCanCreateAt(HomePage, RegionLandingPage)

    def test_landing_page_subpages(self):
        # A IndustryLandingPage can only have other RegionPage children
        self.assertAllowedSubpageTypes(
            RegionLandingPage, {RegionPage})


class RegionPageTests(WagtailPageTests):
    def test_can_create_under_landing_page(self):
        self.assertCanCreateAt(RegionLandingPage, RegionPage)

    def test_region_page_subpages(self):
        # A RegionPage can only have other RegionPage children
        self.assertAllowedSubpageTypes(
            RegionLandingPage, {RegionPage})
