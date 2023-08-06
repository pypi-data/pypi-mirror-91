from hotair.template.element import Element
from hotair.template.node import Node


class CustomElement(Element):
    def __init__(self):
        super().__init__()
        self.inserted = False

    async def setup(self):
        ...

    async def render(self) -> Node:
        return ...
