"""
wagtail.contrib.settings - hold global text and images, e.g. for navbar, social buttons
"""
from django.db import models

from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.images.edit_handlers import ImageChooserPanel


@register_setting
class Branding(BaseSetting):
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('logo'),
    ]
