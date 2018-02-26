from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page
from wagtailmarkdown.fields import MarkdownField


class InfoPage(Page):
    content = MarkdownField()

    content_panels = Page.content_panels + [
        FieldPanel('content'),
    ]
