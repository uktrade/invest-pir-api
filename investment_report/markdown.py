from markdown.extensions.footnotes import FootnoteExtension
from markdown import Markdown


class CustomFootnoteExtension(FootnoteExtension):
    def makeFootnotesDiv(self, root):
        div = super().makeFootnotesDiv(root)

        if div:
            # Put numbers in list text
            notes = div.findall('.//li')
            for i, n in enumerate(notes):
                n[0].text = '{}. {}'.format(i + 1, n[0].text)

        return div


def custom_markdown(a_str, section_counter=0, local=True):
    md = Markdown(extensions=[
        CustomFootnoteExtension(),
    ])

    md.local = local
    str_ = md.convert(a_str)
    str_ = str_.replace('$SECTION', str(section_counter))

    return str_
