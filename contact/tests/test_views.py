import http
from unittest.mock import patch, Mock

import pytest

from zenpy.lib.api_objects import Ticket, User

from contact import forms
from contact.views import FeedbackFormView, ReportIssueFormView


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
