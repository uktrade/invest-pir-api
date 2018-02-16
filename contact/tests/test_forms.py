from contact import forms


def test_feeback_form_required():
    form = forms.FeedbackForm()

    assert form.is_valid() is False
    assert form.fields['name'].required is True
    assert form.fields['email'].required is True
    assert form.fields['feedback'].required is True
    assert form.fields['captcha'].required is True


def test_feeback_form_accepts_valid_data(captcha_stub):
    form = forms.FeedbackForm(
        data={
            'name': 'Jim Example',
            'email': 'jim@example.com',
            'feedback': 'Hello',
            'recaptcha_response_field': captcha_stub
        }
    )
    assert form.is_valid()
