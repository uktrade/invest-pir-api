from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Submit, HTML
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

STAFF_CHOICES = (
    (
        'Less than 10',
        _('Less than 10')
    ),
    (
        '10 to 50',
        _('10 to 50')
    ),
    (
        '51 to 250',
        _('51 to 250')
    ),
    (
        'More than 250',
        _('More than 250')
    ),
)


class ContactForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Contact Information",
                'name',
                'job_title',
                'email',
                'phone_number',
            ),
            Fieldset(
                "Company information",
                'company_name',
                'company_website',
                'country',
                'staff_number',
            ),
            Fieldset(
                "Your plans",
                'description',
            ),
            Field('captcha'),
            HTML("<p>{}</p>".format(
                _(
                    "By sending us your details you can confirm that the "
                    "information you've shared with us is true and you "
                    "accept our terms and conditions."
                )
            )),
            Submit("submit", _("Submit"), css_class='btn btn_primary')
        )
        super().__init__(*args, **kwargs)

    name = forms.CharField(label=_('Name'))
    job_title = forms.CharField(label=_('Job title'))
    email = forms.EmailField(label=_('Email address'))
    phone_number = forms.CharField(
        label=_('Phone number (optional)'),
        required=True

    )

    company_name = forms.CharField(label=_('Company name'))
    company_website = forms.URLField(
        label=_('Website URL'),
        required=False
    )
    country = forms.CharField(
        label=_('Which country are you based in?'),
        help_text=_('We will use this information to put in touch with your'
                    'closest British embassy or high commission.')

    )
    staff_number = forms.ChoiceField(
        label=_('Current number of staff'),
        choices=STAFF_CHOICES
    )
    description = forms.CharField(
        label=_('Tell us about your investment'),
        help_text=_('Tell us about your company and your plans for the UK in '
                    'terms of size of investment, operational and recruitment '
                    'plans. Please also tell us what help you would like from '
                    'the UK government.'),
        widget=forms.Textarea()
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )


class FeedbackForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.add_input(
            Submit("submit", _("Submit"), css_class='btn btn_primary')
        )
        super().__init__(*args, **kwargs)

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


class ReportIssueForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.add_input(
            Submit("submit", _("Submit"), css_class='btn btn_primary')
        )
        super().__init__(*args, **kwargs)

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
