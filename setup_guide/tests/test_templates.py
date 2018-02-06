from django.template.loader import render_to_string


def test_landing_page():
    context = {}
    html = render_to_string(
        "setup_guide/setup_guide_landing_page.html",
        context)
    assert html


def test_guide_page():
    context = {}
    html = render_to_string(
        "setup_guide/setup_guide_page.html",
        context)
    assert html
