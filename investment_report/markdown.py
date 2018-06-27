from django.conf import settings

from markdown.extensions.footnotes import FootnoteExtension
from markdown import Markdown, inlinepatterns


class CustomFootnoteExtension(FootnoteExtension):
    def makeFootnotesDiv(self, root):
        div = super().makeFootnotesDiv(root)

        if div:
            # Put numbers in list text
            notes = div.findall('.//li')
            for i, n in enumerate(notes):
                n[0].text = '{}. {}'.format(i + 1, n[0].text)

        return div


class CustomImagePattern(inlinepatterns.ImagePattern):
    def sanitize_url(self, url):
        url = super().sanitize_url(url)

        if settings.AWS_S3_CUSTOM_DOMAIN:
            url = 'https://{}{}'.format(settings.AWS_S3_CUSTOM_DOMAIN, url)
            return url
        else:
            return url


# Monkey Patch image url
inlinepatterns.ImagePattern = CustomImagePattern


def custom_markdown(a_str, local=True):
    md = Markdown(extensions=[CustomFootnoteExtension()])
    md.local = local
    str_ = md.convert(a_str)
    return str_