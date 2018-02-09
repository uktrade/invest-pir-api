from django.template.loader import render_to_string


def test_landing_page():
    context = {}
    html = render_to_string(
        "sector/sector_landing_page.html",
        context)
    assert html


def test_sector_page():
    context = {}
    html = render_to_string(
        "sector/sector_page.html",
        context)
    assert html
