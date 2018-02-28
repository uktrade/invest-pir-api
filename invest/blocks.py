from django.db.models import SET_NULL
from wagtail.core.blocks import StructBlock, CharBlock
from wagtail_svgmap.blocks import ImageMapBlock
from wagtailmarkdown.blocks import MarkdownBlock


class LocationAccordionItemBlock(StructBlock):
    class Meta:
        template = 'blocks/accordion_item_location.html'

    info = MarkdownBlock()
    map = ImageMapBlock(on_delete=SET_NULL, null=True)


class MarkdownAccordionItemBlock(StructBlock):
    class Meta:
        template = 'blocks/accordion_item_markdown.html'

    # accordion section
    title = CharBlock(max_length=255)
    content = MarkdownBlock()
