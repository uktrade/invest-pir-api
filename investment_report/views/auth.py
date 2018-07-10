import logging

from django.core.urlresolvers import reverse_lazy
from django import forms
from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


class ResetRequestForm(forms.Form):
    username = forms.CharField(required=True)


class ResetRequestView(SuccessMessageMixin, FormView):
    template_name = 'admin/unlock_account.html'
    form_class = ResetRequestForm
    success_url = reverse_lazy('reset_request')
    success_message = (
        "An administrator has emailed requesting to unlock %(email)s"
    )

    def send_email(self, user):
        send_mail(
            'User {} - requesting login reset'.format(user.username),
            (
                'Dear Admin, \n\nUser {} has been locked out of their account'
                ' and is requesting that you unlock them. Please go to the '
                'admin and delete all access logs under their username to'
                'allow them access once more'
            ).format(user.username),
            [settings.RESET_EMAIL]
        )

    def form_valid(self, form):
        username = form.cleaned_data['username']

        User = get_user_model()

        try:
            user = User.objects.get(username=username)
            self.send_email(user)
        except User.DoesNotExist:
            logger.info('Invalid username {}, request reset'.format(username))

        # Still returning the form as valid. Generally good practice not
        # to let people know what emails are in the database. Prevents
        # possible phishing attacks.
        return super().form_valid(form)
