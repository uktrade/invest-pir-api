from .models import SectorPage, SectorLandingPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(SectorPage)
class SectorPageTranslation(TranslationOptions):
    fields = (
        'description',
        'heading',
        'pullout',
        'subsections',
    )


@register(SectorLandingPage)
class SectorLandingPageTranslation(TranslationOptions):
    fields = (
        'heading',
    )
