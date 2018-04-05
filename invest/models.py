"""
wagtail.contrib.settings - hold global text and images, e.g.
for navbar, social buttons
"""
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.blocks import PageChooserBlock
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmarkdown.fields import MarkdownField

from invest.blocks.external_link import ExternalLinkBlock


@register_setting
class Branding(BaseSetting):
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    language_choice_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    footer_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    footer_secondary_nav = StreamField([
        ('internal_link', PageChooserBlock()),
        ('external_link', ExternalLinkBlock()),
         ],
        blank=True)

    footer_copyright = models.CharField(max_length=255)

    is_beta = models.BooleanField(default=True)
    beta_bar_text = MarkdownField(
        default="This is a new service - your feedback will help improve it."
    )

    panels = [
        ImageChooserPanel('logo'),
        ImageChooserPanel('language_choice_icon'),
        ImageChooserPanel('footer_logo'),
        StreamFieldPanel("footer_secondary_nav"),
        FieldPanel('footer_copyright'),
        FieldPanel('is_beta'),
        FieldPanel('beta_bar_text'),
    ]
