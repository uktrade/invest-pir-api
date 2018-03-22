from .models import InfoPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(InfoPage)
class InfoPageTranslation(TranslationOptions):
    fields = (
        'content',
    )
