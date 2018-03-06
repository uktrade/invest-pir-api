from gettext import gettext as _

from django.db.models import CharField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page
from .views import ContactFormView, FeedbackFormView, ReportIssueFormView


class FormViewPage(Page):
    """
    Allow a wagtail Page to render a FormView.
    """
    def __init__(self, view, *args, **kwargs):
        self.view = view
        Page.__init__(self, *args, **kwargs)

    def serve(self, request):
        """
        Populate response with context from wagtail as well as
        FormView

        :param request:
        :return:
        """
        view = self.view.as_view()

        response = view(request)
        response.context_data['page'] = self
        response.context_data['self'] = self
        return response


class ContactFormPage(FormViewPage):
    def __init__(self, *args, **kwargs):
        FormViewPage.__init__(self, ContactFormView, *args, **kwargs)

    heading = CharField(max_length=255, default=_("Contact Us"))

    content_panels = Page.content_panels + [
        FieldPanel('heading')
    ]


class FeedbackFormPage(FormViewPage):
    def __init__(self, *args, **kwargs):
        FormViewPage.__init__(self, FeedbackFormView, *args, **kwargs)

    heading = CharField(max_length=255, default=_("Feedback"))

    content_panels = Page.content_panels + [
        FieldPanel('heading')
    ]


class ReportIssueFormPage(FormViewPage):
    def __init__(self, *args, **kwargs):
        FormViewPage.__init__(self, ReportIssueFormView, *args, **kwargs)

    view = ReportIssueFormView
    heading = CharField(max_length=255, default=_("Report Issue"))

    content_panels = Page.content_panels + [
        FieldPanel('heading')
    ]
