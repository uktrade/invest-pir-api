from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page
from wagtailmarkdown.fields import MarkdownField


class InfoPage(Page):
    """
    Markdown page - used for terms and conditions
    and privacy policy
    """
    content = MarkdownField()

    content_panels = Page.content_panels + [
        FieldPanel('content'),
    ]
