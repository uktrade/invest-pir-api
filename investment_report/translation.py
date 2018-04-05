from investment_report.models import FrontPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(FrontPage)
class SectorPageTranslation(TranslationOptions):
    fields = (
        'content',
    )
