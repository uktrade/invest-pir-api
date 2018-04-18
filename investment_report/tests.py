from django.test import SimpleTestCase

from investment_report.markdown import custom_markdown


class TestCase(SimpleTestCase):
    def test_custom_markdown_image_paths(self):
        res = custom_markdown('![](/media/markdownx/31276d18-1d77-45cd-8842-c4dc31a8536d.png)')
