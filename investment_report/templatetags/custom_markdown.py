from django import template
from investment_report.markdown import custom_markdown


register = template.Library()


@register.simple_tag(takes_context=True)
def increment_section(context):
    if 'section_counter' not in context:
        context['section_counter'] = 1
    else:
        context['section_counter'] = context['section_counter'] + 1

    return ''


@register.simple_tag(takes_context=True)
def markdown(context, markdown_field):
    return custom_markdown(
        markdown_field,
        section_counter=context.get('section_counter', 1),
        local=context['local']
    )
