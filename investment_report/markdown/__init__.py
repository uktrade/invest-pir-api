from markdown.extensions.footnotes import *
from markdown import util


class CustomFootnoteExtension(FootnoteExtension):
    def makeFootnotesDiv(self, root):
        div = super().makeFootnotesDiv(root)
        
        if div:
            # Put numbers in list text
            notes = div.findall('.//li')
            for i, n in enumerate(notes):
                n[0].text = '{}. {}'.format(i + 1, n[0].text)

        return div
