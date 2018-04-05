import http
from unittest.mock import patch, Mock

import pytest

from zenpy.lib.api_objects import Ticket, User

from contact import forms
from contact.models import ContactFormPage, FeedbackFormPage, \
    ReportIssueFormPage
from contact.views import ContactFormView, FeedbackFormView, \
    ReportIssueFormView


@pytest.fixture
def report_issue_form_data():
    return {
        'name': 'Jim Example',
        'email': 'jim@example.com',
        'feedback': 'Test feedback',
    }


@pytest.fixture
def report_issue_request(rf, client, report_issue_form_data):
    request = rf.post('/', report_issue_form_data)
    request.session = client.session
    return request


@pytest.mark.django_db
@patch('zenpy.lib.api.UserApi.create_or_update')
@patch('zenpy.lib.api.TicketApi.create')
@patch('captcha.fields.ReCaptchaField.clean')
def test_lead_generation_view_submit_with_comment(
    mock_clean_captcha, mock_ticket_create, mock_user_create_or_update,
    report_issue_request, report_issue_form_data
):
    mock_user_create_or_update.return_value = Mock(id=999)
    response = ReportIssueFormView.as_view()(report_issue_request)

    assert response.status_code == http.client.OK
    assert response.template_name == ReportIssueFormView.success_template

    assert mock_user_create_or_update.call_count == 1
    user = mock_user_create_or_update.call_args[0][0]
    assert user.__class__ == User
    assert user.email == report_issue_form_data['email']
    assert user.name == report_issue_form_data['name']

    assert mock_ticket_create.call_count == 1
    ticket = mock_ticket_create.call_args[0][0]
    assert ticket.__class__ == Ticket
    assert ticket.subject == 'Invest feedback'
    assert ticket.submitter_id == 999
    assert ticket.requester_id == 999
    description = (
        'Name: {name}\n'
        'Email: {email}\n'
        'Feedback: {feedback}'
    ).format(**report_issue_form_data)
    assert ticket.description == description
    assert mock_clean_captcha.call_count == 1


@pytest.fixture
def feedback_form_data():
    return {
        'name': 'Jim Example',
        'email': 'jim@example.com',
        'feedback': 'Test feedback',
        'service_quality': forms.FEEDBACK_SERVICE[0][0],
    }


@pytest.fixture
def feedback_request(rf, client, feedback_form_data):
    request = rf.post('/', feedback_form_data)
    request.session = client.session
    return request


@pytest.mark.django_db
@patch('zenpy.lib.api.UserApi.create_or_update')
@patch('zenpy.lib.api.TicketApi.create')
@patch('captcha.fields.ReCaptchaField.clean')
def test_feedback_form(
    mock_clean_captcha, mock_ticket_create, mock_user_create_or_update,
    feedback_request, feedback_form_data
):
    mock_user_create_or_update.return_value = Mock(id=999)
    response = FeedbackFormView.as_view()(feedback_request)

    assert response.status_code == http.client.OK
    assert response.template_name == FeedbackFormView.success_template

    assert mock_user_create_or_update.call_count == 1
    user = mock_user_create_or_update.call_args[0][0]
    assert user.__class__ == User
    assert user.email == feedback_form_data['email']
    assert user.name == feedback_form_data['name']

    assert mock_ticket_create.call_count == 1
    ticket = mock_ticket_create.call_args[0][0]
    assert ticket.__class__ == Ticket
    assert ticket.subject == 'Invest feedback'
    assert ticket.submitter_id == 999
    assert ticket.requester_id == 999
    description = (
        'Name: {name}\n'
        'Email: {email}\n'
        'Service quality: {service_quality}\n'
        'Feedback: {feedback}'
    ).format(**feedback_form_data)
    assert ticket.description == description
    assert mock_clean_captcha.call_count == 1


@pytest.fixture
def contact_form_data():
    return {
            'name': 'Scrooge McDuck',
            'email': 'sm@example.com',
            'job_title': 'President',
            'phone_number': '0000000000',
            'company_name': 'Acme',
            'country': 'Duckburg',
            'staff_number': forms.STAFF_CHOICES[0][0],
            'description': 'foobar',
    }


@pytest.fixture
def contact_request(rf, client, contact_form_data):
    request = rf.post('/', contact_form_data)
    request.session = client.session
    return request


@pytest.fixture
def contact_page():
    return ContactFormPage(heading="Test Contact Heading")


@pytest.fixture
def feedback_page():
    return FeedbackFormPage(heading="Test Feedback Heading")


@pytest.fixture
def report_issue_page():
    return ReportIssueFormPage(heading="Test Report Issue Heading")


@pytest.mark.django_db
@patch('zenpy.lib.api.UserApi.create_or_update')
@patch('zenpy.lib.api.TicketApi.create')
@patch('captcha.fields.ReCaptchaField.clean')
def test_contact_form(
    mock_clean_captcha, mock_ticket_create, mock_user_create_or_update,
    contact_request, contact_form_data
):
    mock_user_create_or_update.return_value = Mock(id=999)
    response = ContactFormView.as_view()(contact_request)

    assert response.status_code == http.client.OK
    assert response.template_name == ContactFormView.success_template

    assert mock_user_create_or_update.call_count == 1
    user = mock_user_create_or_update.call_args[0][0]
    assert user.__class__ == User
    assert user.email == contact_form_data['email']
    assert user.name == contact_form_data['name']

    assert mock_ticket_create.call_count == 1
    ticket = mock_ticket_create.call_args[0][0]
    assert ticket.__class__ == Ticket
    assert ticket.subject == 'Invest feedback'
    assert ticket.submitter_id == 999
    assert ticket.requester_id == 999
    contact_form_data['company_website'] = ''
    contact_form_data['phone_number'] = '0000000000'
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
    ).format(**contact_form_data)
    assert ticket.description == description
    assert mock_clean_captcha.call_count == 1


@pytest.mark.django_db
def test_contact_page_serve(contact_page, contact_request):
    response = contact_page.serve(contact_request)
    context = response.context_data

    assert context["page"] == contact_page
    assert context["self"] == contact_page


@pytest.mark.django_db
def test_feedback_page_serve(feedback_page, contact_request):
    response = feedback_page.serve(contact_request)
    context = response.context_data

    assert context["page"] == feedback_page
    assert context["self"] == feedback_page


@pytest.mark.django_db
def test_report_issue_page_serve(report_issue_page, contact_request):
    response = report_issue_page.serve(contact_request)
    context = response.context_data

    assert context["page"] == report_issue_page
    assert context["self"] == report_issue_page
