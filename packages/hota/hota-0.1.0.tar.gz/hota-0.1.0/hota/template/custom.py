from hota.template.element import Element
from hota.template.node import Node


class CustomElement(Element):
    def __init__(self):
        super().__init__()
        self.inserted = False

    async def setup(self):
        ...

    async def render(self) -> Node:
        return ...
