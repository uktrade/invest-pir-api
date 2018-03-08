from wagtail.core.blocks import CharBlock, URLBlock, StructBlock


class ExternalLinkBlock(StructBlock):
    class Meta:
        icon = 'link'
        label = 'External Link'
        template = 'blocks/external_link.html'

    link = URLBlock(max_length=255)
    text = CharBlock(max_length=255)

    def is_live(self):
        """
        Provide is_live so the block behaves in the same way
        as internal page links.

        :return:
        """
        return True