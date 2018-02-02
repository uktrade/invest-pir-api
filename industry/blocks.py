from wagtail.core.blocks import StructBlock, CharBlock
from wagtailmarkdown.blocks import MarkdownBlock


class MarkdownAccordionItemBlock(StructBlock):
    class Meta:
        template = 'industry/blocks/accordion/markdown_item.html'

    # accordion section
    title = CharBlock(max_length=255)
    content = MarkdownBlock()
