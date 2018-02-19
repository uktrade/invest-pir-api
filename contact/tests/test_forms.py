from contact import forms


def test_report_issue_form_required():
    form = forms.ReportIssueForm()

    assert form.is_valid() is False
    assert form.fields['name'].required is True
    assert form.fields['email'].required is True
    assert form.fields['feedback'].required is True
    assert form.fields['captcha'].required is True


def test_report_issue_form_accepts_valid_data(captcha_stub):
    form = forms.ReportIssueForm(
        data={
            'name': 'Jim Example',
            'email': 'jim@example.com',
            'feedback': 'Hello',
            'recaptcha_response_field': captcha_stub
        }
    )
    assert form.is_valid()


def test_feedback_form_required():
    form = forms.FeedbackForm()

    assert form.is_valid() is False
    assert form.fields['name'].required is True
    assert form.fields['email'].required is True
    assert form.fields['service_quality'].required is True
    assert form.fields['feedback'].required is True
    assert form.fields['captcha'].required is True


def test_feedback_accepts_valid_data(captcha_stub):
    form = forms.FeedbackForm(
        data={
            'name': 'Jim Example',
            'email': 'jim@example.com',
            'service_quality': forms.FEEDBACK_SERVICE[0][0],
            'feedback': 'Hello',
            'recaptcha_response_field': captcha_stub
        }
    )
    assert form.is_valid()
