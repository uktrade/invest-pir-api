from wagtail.tests.utils import WagtailPageTests
from sector.models import SectorLandingPage, SectorPage
from home.models import HomePage


class SectorLandingPageTests(WagtailPageTests):
    def test_can_create_under_homepage(self):
        self.assertCanCreateAt(HomePage, SectorLandingPage)

    def test_landing_page_subpages(self):
        # A IndustryLandingPage can only have other SectorPage children
        self.assertAllowedSubpageTypes(
            SectorLandingPage, {SectorPage})


class SectorPageTests(WagtailPageTests):
    def test_can_create_under_landing_page(self):
        self.assertCanCreateAt(SectorLandingPage, SectorPage)

    def test_sector_page_subpages(self):
        # A SectorPage can only have other SectorPage children
        self.assertAllowedSubpageTypes(
            SectorLandingPage, {SectorPage})
