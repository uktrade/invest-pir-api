import markdown


def markdown_fragment(a_str):
    return markdown.markdown(a_str, extensions=['markdown.extensions.footnotes'])
