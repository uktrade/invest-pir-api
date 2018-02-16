from captcha.fields import ReCaptchaField
from django import forms
from django.utils.translation import ugettext as _

from directory_validators.common import not_contains_url_or_email
from directory_validators.company import no_html


class ReportIssueForm(forms.Form):
    name = forms.CharField(label=_('Name'))
    email = forms.EmailField(label=_('Email'))
    feedback = forms.CharField(
        label=_('Feedback'),
        help_text=_('Maximum 1200 characters.'),
        max_length=1200,
        widget=forms.Textarea,
        validators=[no_html, not_contains_url_or_email]
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )
