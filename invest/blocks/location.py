from wagtail.core.blocks import StructBlock, CharBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailmarkdown.blocks import MarkdownBlock


class LocationAccordionItemBlock(StructBlock):
    class Meta:
        template = 'blocks/accordion_item_location.html'

    # accordion section
    title = CharBlock(max_length=255)
    info = MarkdownBlock()
    map = ImageChooserBlock()
