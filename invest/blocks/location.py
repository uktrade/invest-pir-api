from django.db.models import CASCADE
from wagtail.core.blocks import StructBlock
from wagtail_svgmap.blocks import ImageMapBlock
from wagtailmarkdown.blocks import MarkdownBlock


class LocationAccordionItemBlock(StructBlock):
    class Meta:
        template = 'blocks/accordion_item_location.html'

    info = MarkdownBlock()
    map = ImageMapBlock(on_delete=CASCADE, null=True)
