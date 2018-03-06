from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket, User as ZendeskUser

from django.conf import settings
from django.template.response import TemplateResponse
from django.views.generic.edit import FormView
from django.utils.translation import ugettext as _


from contact import forms


ZENPY_CREDENTIALS = {
    'email': settings.ZENDESK_EMAIL,
    'token': settings.ZENDESK_TOKEN,
    'subdomain': settings.ZENDESK_SUBDOMAIN
}
# Zenpy will let the connection timeout after 5s and will retry 3 times
zenpy_client = Zenpy(timeout=5, **ZENPY_CREDENTIALS)


class FormViewMixin:
    """
    Allow a wagtail Page to render a FormView.

    Usage:  set view attribute to FormView class

    class SomeFormPage(FormViewMixin, Page):
        view = SomeFormView
        ....

    Provides a serve(...) method.   Must be appear before
    Page in list of superclasses to override serve
    """
    def __init__(self, *args, **kwargs):
        assert getattr(self, "view") is not None, \
            f"No view supplied to {self}"
        super().__init__(*args, **kwargs)

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


class ZendeskView:

    def create_description(self, data):
        raise NotImplementedError

    def create_zendesk_ticket(self, description, zendesk_user):
        ticket = Ticket(
            subject='Invest feedback',
            description=description,
            submitter_id=zendesk_user.id,
            requester_id=zendesk_user.id,
        )
        zenpy_client.tickets.create(ticket)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success_message'] = _('Your feedback has been submitted')
        return context

    @staticmethod
    def get_or_create_zendesk_user(name, email):
        zendesk_user = ZendeskUser(
            name=name,
            email=email,
        )
        return zenpy_client.users.create_or_update(zendesk_user)

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        zendesk_user = self.get_or_create_zendesk_user(name, email)
        description = self.create_description(form.cleaned_data)
        self.create_zendesk_ticket(description, zendesk_user)
        return TemplateResponse(self.request, self.success_template)


class ReportIssueFormView(ZendeskView, FormView):
    success_template = 'report_issue_success.html'
    template_name = 'contact/report_issue.html'
    form_class = forms.ReportIssueForm

    def create_description(self, data):
        description = (
            'Name: {name}\n'
            'Email: {email}\n'
            'Feedback: {feedback}'
        ).format(**data)
        return description

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success_message'] = _(
            "Your details have been submitted and will be reviewed by our "
            "team.  "
            "If we need more information from you, we'll contact you within "
            "5 working days."
        )
        return context


class FeedbackFormView(ZendeskView, FormView):
    success_template = 'feedback-success.html'
    template_name = 'contact/feedback.html'
    form_class = forms.FeedbackForm

    def create_description(self, data):
        description = (
            'Name: {name}\n'
            'Email: {email}\n'
            'Service quality: {service_quality}\n'
            'Feedback: {feedback}'
        ).format(**data)
        return description


class ContactFormView(ZendeskView, FormView):
    success_template = 'contact-success.html'
    template_name = 'contact/contact.html'
    form_class = forms.ContactForm

    def create_description(self, data):

        # handle not required fields
        if 'phone_number' not in data:
            data['phone_number'] = ''
        if 'company_website' not in data:
            data['company_website'] = ''

        description = (
            'Name: {name}\n'
            'Email: {email}\n'
            'Job title: {job_title}\n'
            'Phone number: {phone_number}\n'
            'Company name: {company_name}\n'
            'Company website: {company_website}\n'
            'Country: {country}\n'
            'Staff number: {staff_number}\n'
            'Investment description: {description}'
        ).format(**data)
        return description
