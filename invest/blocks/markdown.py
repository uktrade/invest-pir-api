from wagtail.core.blocks import StructBlock, CharBlock
from wagtailmarkdown.blocks import MarkdownBlock


class MarkdownAccordionItemBlock(StructBlock):
    class Meta:
        template = 'blocks/accordion_item_markdown.html'

    # accordion section
    title = CharBlock(max_length=255)
    content = MarkdownBlock()
