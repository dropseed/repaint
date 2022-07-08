import asyncio
import json
import os
from typing import List

import websockets
from cached_property import cached_property

from .events import BROWSER_RELOAD, BROWSER_RELOAD_ASSETS
from .server import Server


class Repaint:
    def __init__(self, port=None, quiet=False):
        self.port = os.environ.get("REPAINT_PORT", 8765)
        self.server = Server(port=self.port, quiet=quiet)

    @cached_property
    def script_tag(self):
        script_path = os.path.join(os.path.dirname(__file__), "js", "browser.js")
        with open(script_path, "r") as f:
            script_contents = f.read()

        return f"""<script data-repaint-port="{self.port}">{script_contents}</script>"""

    def _send_reload(self, event_data: dict):
        async def send_reload(data: dict):
            uri = f"ws://localhost:{self.port}"
            json_data = json.dumps(data)
            async with websockets.connect(uri) as websocket:
                await websocket.send(json_data)

        asyncio.run(send_reload(event_data))

    def reload(self):
        """
        Send a reload event directly back to the websocket server
        (can be called by any Python code outside the server itself)
        """
        self._send_reload({"type": BROWSER_RELOAD})

    def reload_assets(self, assets: List[str] = []):
        self._send_reload({"type": BROWSER_RELOAD_ASSETS, "assets": assets})
