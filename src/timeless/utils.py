
import textwrap


def generate_indented_repr(first, body, last, prefix=4 * " ", trailing_comma=True):
    if trailing_comma:
        body += ","
    return "\n".join([first, textwrap.indent(body, prefix=prefix), last])
