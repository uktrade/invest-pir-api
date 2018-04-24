import os

from django import template
from django.templatetags.static import static
from django.conf import settings
from django.urls import reverse


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


@register.simple_tag(takes_context=True)
def markdown(context, markdown_field):
    from investment_report.markdown import custom_markdown
    return custom_markdown(markdown_field, local=context['local'])


@register.simple_tag
def is_report_availible(reports, lang, market, sector):
    detail_url = reverse('reportadmin:validation_table_detail', args=(lang, market, sector,))


    if sector in reports.get(lang, {}).get(market, []):
        return '<td><a href="{}">💚</a></td>'.format(detail_url)
    else:
        return '<td><a href="{}">❌</a></td>'.format(detail_url)
