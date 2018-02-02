from django.template.loader import render_to_string


def test_landing_page():
    context = {}
    html = render_to_string(
        "industry/industries_landing_page.html",
        context)
    assert html


def test_industry_page():
    context = {}
    html = render_to_string(
        "industry/industry_page.html",
        context)
    assert html
