from .models import ContactFormPage, FeedbackFormPage, ReportIssueFormPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(ContactFormPage)
class ContactFormPageTranslation(TranslationOptions):
    fields = (
        'heading',
    )


@register(FeedbackFormPage)
class FeedbackFormPageTranslation(TranslationOptions):
    fields = (
        'heading',
    )


@register(ReportIssueFormPage)
class ReportIssueFormPageTranslation(TranslationOptions):
    fields = (
        'heading',
    )
