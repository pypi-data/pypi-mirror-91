from starlette.types import Receive, Scope, Send
from starlette.websockets import WebSocket

from .template.dom import DOM


class HTMLOverTheAirWebSocket(WebSocket):
    def __init__(self, scope: Scope, receive: Receive, send: Send) -> None:
        super().__init__(scope, receive, send)
        self.handlers = {}
        self.frame_to_element = {}

    @property
    def dom(self) -> DOM:
        return DOM(ws=self)

    async def run(self):
        while True:
            data = await self.receive_json()

            if data['type'] == 4:
                uuid = data['uuid']
                handler = self.handlers.get(uuid)
                if handler:
                    await handler()
                    (json_data, node) = await self.dom._render_for(data['frame'], handler.__self__, type=2)
                    await self.send_json(json_data)
                    await self.send_text(node.serialised())


class HTMLOverTheAirEndpoint:
    def __init__(self, on_accept=None):
        self.on_accept = on_accept

    async def __call__(self, scope, receive, send):
        websocket = HTMLOverTheAirWebSocket(
            scope=scope, receive=receive, send=send)
        await websocket.accept()
        if self.on_accept:
            await self.on_accept(websocket)
        await websocket.run()
