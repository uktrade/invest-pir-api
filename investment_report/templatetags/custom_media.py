from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def custom_media(context, file_field):
    """
    Convenience tag to prevent

        {% if model.image %}{{ model.image.url }}{% endif %}

    being littered everywhere and harming readability.
    """
    if file_field:
        return file_field.url
    return ''


@register.simple_tag
def header_color(model, attr=None):
    attr = attr or 'color'
    if hasattr(model, 'header_color') and model.header_color:
        return ' style="{}: {};" '.format(attr, model.header_color)
    return ''
