import markdown

from bs4 import BeautifulSoup
from investment_report.models import PDFSection


def bs_parse(html):
    return BeautifulSoup(html, 'html.parser')


def markdown_fragment(a_str):
    return markdown.markdown(a_str, extensions=['markdown.extensions.footnotes'])


def investment_report_generator(market, sector):
    document = bs_parse('<body></body>')

    for klass in PDFSection.__subclasses__():

        if hasattr(klass, 'sector'):
            page = klass.objects.filter(sector=sector).first()
        elif hasattr(klass, 'market'):
            page = klass.objects.filter(market=market).first()
        else:
            page = klass.objects.first()

        if page:
            page_section = bs_parse('<section></section>')
            page_section.section['class'] = page._meta.model_name

            page_section.section.append(
                bs_parse(page.to_html_fragment())
            )

            document.body.append(page_section)

    return document
