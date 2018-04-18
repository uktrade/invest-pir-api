import os

from django import template
from django.templatetags.static import static
from django.conf import settings


register = template.Library()


@register.simple_tag(takes_context=True)
def custom_static(context, format_string):
    if 'local' in context and context['local'] == True:
        return 'file://' + os.path.join(settings.STATIC_ROOT, format_string)

    return static(format_string)


@register.simple_tag(takes_context=True)
def custom_media(context, file_field):
    if 'local' in context and context['local'] == True:
        return 'file://' + file_field.path

    return file_field.url
