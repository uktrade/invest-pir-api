from investment_report.models import PDFSection
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


for klass in PDFSection.__subclasses__():
    @register(klass)
    class PageTranslation(TranslationOptions):
        fields = (
            'content',
        )
