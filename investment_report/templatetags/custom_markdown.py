import os

from django import template
from django.templatetags.static import static
from django.conf import settings
from django.urls import reverse
from investment_report.markdown import custom_markdown


register = template.Library()


@register.simple_tag(takes_context=True)
def markdown(context, markdown_field):
    return custom_markdown(markdown_field, local=context['local'])
