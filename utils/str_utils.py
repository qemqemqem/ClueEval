import textwrap

def unindent(text: str) -> str:
    """
    Remove any common leading whitespace from every line in text.
    
    This can be used to make triple-quoted strings line up with the left edge of
    the display, while still presenting them in the source code in indented form
    for readability.
    """
    return textwrap.dedent(text).strip()
