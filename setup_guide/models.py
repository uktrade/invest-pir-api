from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from invest.blocks import MarkdownAccordionItemBlock


class SetupGuideLandingPage(Page):
    # page fields
    heading = models.CharField(max_length=255)
    sub_heading = models.CharField(max_length=255)

    content_panels = Page.content_panels + [
        FieldPanel('heading'),
        FieldPanel('sub_heading'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['setup_guide_cards'] = SetupGuide.objects.live()
        return context


class SetupGuide(Page):
    description = models.TextField()  # appears in card on external pages

    heading = models.CharField(max_length=255)
    sub_heading = models.CharField(max_length=255)

    # accordion
    subsections = StreamField([
        ('markdown', MarkdownAccordionItemBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('heading'),
        FieldPanel('sub_heading'),
        StreamFieldPanel('subsections')
    ]
