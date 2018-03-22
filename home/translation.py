from .models import HomePage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(HomePage)
class HomePageTranslation(TranslationOptions):
    fields = (
        'heading',
        'sub_heading',
        'subsections',
        'sector_title',
        'setup_guide_title',
        'setup_guide_lead_in',
        'how_we_help_title',
        'how_we_help',
    )
