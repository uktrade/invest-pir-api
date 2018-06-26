from django import template
from investment_report.markdown import custom_markdown


register = template.Library()


@register.simple_tag(takes_context=True)
def markdown(context, markdown_field):
    return custom_markdown(markdown_field, local=context['local'])
