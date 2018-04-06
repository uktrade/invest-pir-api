import pytest

from django.urls import resolve


def mk_page_data(name):
    return dict(
        title_en=name,
        slug_en=name,
        heading_en="test_%s heading" %name,
        description_en="%s description" % name,
    )


LANDING_DATA = mk_page_data('industries')
SECTOR_DATA_1 = mk_page_data('aerospace')
SECTOR_DATA_2 = mk_page_data('creative')


@pytest.mark.django_db
def test_setup_guide_landing_page(client):
    from sector.models import SectorPage, SectorLandingPage
    from wagtail.core.models import Page

    root = Page.objects.filter(pk=1).get()
    home = Page.objects.get(id=3)  # or better Page query

    landing = SectorLandingPage(**LANDING_DATA)
    home.add_child(instance=landing)

    sector1 = SectorPage(**SECTOR_DATA_1)
    sector2 = SectorPage(**SECTOR_DATA_2)

    landing.add_child(instance=sector1)
    landing.add_child(instance=sector2)


    response = client.get('/industries/')
    wsgi_request = response.wsgi_request

    path_components = '/industries'.split('/')
    route = root.specific.route(wsgi_request, path_components)
    assert route.page == landing

    #import ipdb; ipdb.set_trace()
