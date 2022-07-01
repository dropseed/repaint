import asyncio
import json
import os

import websockets
from cached_property import cached_property

from .server import Server


class Repaint:
    def __init__(self, port=8765):
        self.port = port
        self.server = Server(port=port)

    @cached_property
    def script_tag(self):
        script_path = os.path.join(os.path.dirname(__file__), "js", "browser.js")
        with open(script_path, "r") as f:
            script_contents = f.read()

        return f"""<script data-port="{self.port}">{script_contents}</script>"""

    def reload(self):
        """
        Send a reload event directly back to the websocket server
        (can be called by any Python code outside the server itself)
        """

        async def send_reload():
            uri = f"ws://localhost:{self.port}"
            async with websockets.connect(uri) as websocket:
                await websocket.send(json.dumps({"type": "reload"}))

        asyncio.run(send_reload())
