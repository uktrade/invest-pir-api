from captcha.fields import ReCaptchaField
from django import forms
from django.utils.translation import ugettext as _

from directory_validators.common import not_contains_url_or_email
from directory_validators.company import no_html

FEEDBACK_SERVICE = (
    (
        'Very satisfied',
        _('Very satisfied')
    ),
    (
        'Satisfied',
        _('Satisfied')
    ),
    (
        'Neither satisfied or dissatisfied',
        _('Neither satisfied or dissatisfied', )
    ),
    (
        'Dissatisfied',
        _('Dissatisfied')
    ),
    (
        'Very dissatisfied',
        _('Very dissatisfied')
    )
)


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


class FeedbackForm(forms.Form):
    name = forms.CharField(label=_('Name'))
    email = forms.EmailField(label=_('Email'))
    service_quality = forms.ChoiceField(
        widget=forms.RadioSelect,
        label=_('How did you feel about the service you received today?'),
        choices=FEEDBACK_SERVICE
    )
    feedback = forms.CharField(
        label=_('How could we improve this service?'),
        help_text=_(
            'Please don\'t include any personal or financial information, '
            'for example your National Insurance or credit card numbers.'),
        widget=forms.Textarea
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )
