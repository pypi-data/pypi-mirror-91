from xml.sax.saxutils import escape, unescape

from .node import Node

html_escape_table = {
    '"': "&quot;",
    "'": "&apos;"
}


class Text(Node):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self) -> str:
        return f"Text[{self.value!r}]"

    def serialised(self) -> str:
        return escape(self.value, html_escape_table)
