from .models import SetupGuidePage, SetupGuideLandingPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(SetupGuidePage)
class SetupGuidePageTranslation(TranslationOptions):
    fields = (
        'description',
        'heading',
        'sub_heading',
        'subsections',
    )


@register(SetupGuideLandingPage)
class SetupGuideLandingPageTranslation(TranslationOptions):
    fields = (
        'heading',
        'sub_heading',
        'lead_in',
    )
