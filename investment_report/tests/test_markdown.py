from bs4 import BeautifulSoup
from django.test import SimpleTestCase
from investment_report.markdown import custom_markdown


class TestCase(SimpleTestCase):
    def test_custom_markdown_image_paths(self):
        res1 = custom_markdown('![](/media/markdownx/test.png)', local=True)
        self.assertEquals(
            res1,
            '<p><img alt="" src="file:///media/markdownx/test.png" /></p>'
        )

        with self.settings(AWS_S3_CUSTOM_DOMAIN='test'):
            res2 = custom_markdown(
                '![](/media/markdownx/test.png)', local=False
            )

            self.assertEquals(
                res2, (
                    '<p><img alt="" src="https://test'
                    '/media/markdownx/test.png" /></p>'
                )
            )

        with self.settings(AWS_S3_CUSTOM_DOMAIN=None):
            res2 = custom_markdown(
                '![](/media/markdownx/test.png)', local=False
            )

            self.assertEquals(
                res2, '<p><img alt="" src="/media/markdownx/test.png" /></p>'
            )

    def test_custom_markdwon_footnotes(self):
        result = custom_markdown(
            (
                'Text to cite[^1]'
                'Text to cite[^2]'
                '\n\n'
                '[^1]: Cite'
                '\n\n'
                '[^2]: Cite'
            ), local=False
        )

        soup = BeautifulSoup(result, 'html.parser')
        # Assert a numbered list is inserted inside the div (list position
        # didn't work to well for layout in this case)
        self.assertTrue(soup.findAll('p')[1].text.startswith('1.'))
        self.assertTrue(soup.findAll('p')[2].text.startswith('2.'))
