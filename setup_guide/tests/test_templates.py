import pytest

from django.template.loader import render_to_string
from wagtail.core.models import Site

# TODO - these are currently integration tests, they need splitting out
#        to test each template.


@pytest.mark.django_db
def test_setup_guide_landing_page(client):
    response = client.get('/setup_guide/')
    wsgi_request = response.wsgi_request
    wsgi_request.site = Site.find_for_request(wsgi_request)
    context = {
        'request': wsgi_request,
        "setup_guide_cards": []
    }
    html = render_to_string(
        "sector/sector_landing_page.html",
        context,
        request=wsgi_request)
    assert html


@pytest.mark.django_db
def test_setup_guide_page(client):
    response = client.get('/uk-setup-guide/set-company-uk/')
    wsgi_request = response.wsgi_request
    wsgi_request.site = Site.find_for_request(wsgi_request)
    context = {
        'request': wsgi_request,
        "setup_guide_cards": []
    }
    html = render_to_string(
        "sector/sector_landing_page.html",
        context,
        request=wsgi_request)
    assert html
