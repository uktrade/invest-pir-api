from investment_report.models import SectorOverview
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(SectorOverview)
class SectorPageTranslation(TranslationOptions):
    fields = (
        'content',
    )
