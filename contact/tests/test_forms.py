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


def test_contact_form_required():
    form = forms.ContactForm()

    assert form.is_valid() is False
    assert form.fields['name'].required is True
    assert form.fields['email'].required is True
    assert form.fields['job_title'].required is True
    assert form.fields['phone_number'].required is False
    assert form.fields['company_name'].required is True
    assert form.fields['company_website'].required is False
    assert form.fields['country'].required is True
    assert form.fields['staff_number'].required is True
    assert form.fields['description'].required is True
    assert form.fields['captcha'].required is True


def test_contact_form_accept_valid_data(captcha_stub):
    form = forms.ContactForm(
        data={
            'name': 'Scrooge McDuck',
            'email': 'sm@example.com',
            'job_title': 'President',
            'company_name': 'Acme',
            'country': 'Duckburg',
            'staff_number': forms.STAFF_CHOICES[0][0],
            'description': 'foobar',
            'recaptcha_response_field': captcha_stub
        }
    )
    assert form.is_valid()
