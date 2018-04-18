import os

from django.conf import settings

from markdown.extensions.footnotes import *
from markdown import util
from markdown import inlinepatterns


class CustomFootnoteExtension(FootnoteExtension):
    def makeFootnotesDiv(self, root):
        div = super().makeFootnotesDiv(root)
        
        if div:
            # Put numbers in list text
            notes = div.findall('.//li')
            for i, n in enumerate(notes):
                n[0].text = '{}. {}'.format(i + 1, n[0].text)

        return div


class ImagePattern(inlinepatterns.ImagePattern):
    def sanitize_url(self, url):
        url = super().sanitize_url(url)
        if self.markdown.local:
            if url.startswith(settings.MEDIA_URL):
                url = url[len(settings.MEDIA_URL):]

            return 'file://' + os.path.join(settings.MEDIA_ROOT, url)

        return url

# Monkey Patch image url
inlinepatterns.ImagePattern = ImagePattern
from markdown import Markdown

def custom_markdown(a_str, local=True):
    md = Markdown(extensions=[CustomFootnoteExtension()])
    md.local = local
    str_ = md.convert(a_str)
    return str_
