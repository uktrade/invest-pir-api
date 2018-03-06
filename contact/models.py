from gettext import gettext as _

from django.db.models import CharField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page
from .views import FormViewMixin, \
    ContactFormView, FeedbackFormView, ReportIssueFormView


class ContactFormPage(FormViewMixin, Page):
    view = ContactFormView
    heading = CharField(max_length=255, default=_("Contact Us"))

    content_panels = Page.content_panels + [
        FieldPanel('heading')
    ]


class FeedbackFormPage(FormViewMixin, Page):
    view = FeedbackFormView
    heading = CharField(max_length=255, default=_("Feedback"))

    content_panels = Page.content_panels + [
        FieldPanel('heading')
    ]


class ReportIssueFormPage(FormViewMixin, Page):
    view = ReportIssueFormView
    heading = CharField(max_length=255, default=_("Report Issue"))

    content_panels = Page.content_panels + [
        FieldPanel('heading')
    ]
