from .models import ContactFormPage, FeedbackFormPage, ReportIssueFormPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(ContactFormPage)
class SetupGuidePageTranslation(TranslationOptions):
    fields = (
        'heading',
    )


@register(FeedbackFormPage)
class SetupGuidePageTranslation(TranslationOptions):
    fields = (
        'heading',
    )


@register(ReportIssueFormPage)
class SetupGuidePageTranslation(TranslationOptions):
    fields = (
        'heading',
    )
