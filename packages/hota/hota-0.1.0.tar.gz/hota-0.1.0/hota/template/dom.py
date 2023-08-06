from uuid import uuid4

from starlette.websockets import WebSocket

from .custom import CustomElement
from .element import Element
from .internal import hota_ack, hota_frame, hota_payload
from .utils import make_nonce


class DOM:
    def __init__(self, *, ws: WebSocket):
        self.ws = ws

    def _accumulate_handlers(self, node):
        for n in node.children:
            if isinstance(n, Element):
                self.ws.handlers.update(n.uuid_to_handler)
                self._accumulate_handlers(n)

    async def _render_for(self, id: str, element: CustomElement, *, type=1):
        nonce = make_nonce()

        if type == 1:
            element_instance = element()
            await element_instance.setup()
            node = await element_instance.render()
            self.ws.handlers.update(element_instance.uuid_to_handler)
            self.ws.handlers.update(node.uuid_to_handler)
            frame = hota_frame(id=str(uuid4()))[node]
            self.ws.frame_to_element[frame.id] = node
        else:
            node = await element.render()
            self.ws.handlers.update(element.uuid_to_handler)
            self.ws.handlers.update(node.uuid_to_handler)
            frame = hota_frame(id=id)[node]
        self._accumulate_handlers(node)

        return (
            {
                "type": type,
                "for": id,
                "nack": nonce
            },
            hota_payload[hota_ack[nonce], frame]
        )

    async def render(self, element: CustomElement, *, id='__hota'):
        (json_data, node) = await self._render_for(id, element)
        await self.ws.send_json(json_data)
        await self.ws.send_text(node.serialised())
