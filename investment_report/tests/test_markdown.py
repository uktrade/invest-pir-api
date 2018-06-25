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
