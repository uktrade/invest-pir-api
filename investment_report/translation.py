from investment_report.models import PDFSection, Market, Sector, SectorOverview
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


for klass in PDFSection.__subclasses__() + [Sector]:
    @register(klass)
    class PageTranslation(TranslationOptions):
        fields = tuple(klass.TRANSLATION_FIELDS)
