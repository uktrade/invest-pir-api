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
