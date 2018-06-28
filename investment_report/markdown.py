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


def custom_markdown(a_str, local=True):
    md = Markdown(extensions=[CustomFootnoteExtension()])
    md.local = local
    str_ = md.convert(a_str)
    return str_
