import asyncio
import json
import os

import websockets

from .events import BROWSER_CONNECT, BROWSER_RELOAD, BROWSER_RELOAD_ASSETS


class RepaintBrowser:
    def __init__(self, id, websocket):
        self.id = id
        self.websocket = websocket

    def __str__(self):
        return str(self.id)

    async def send(self, data):
        json_data = json.dumps(data)
        try:
            await self.websocket.send(json_data)
        except websockets.ConnectionClosedError:
            # Retry once
            await self.websocket.send(json_data)


class RepaintServer:
    def __init__(self, port, quiet=False):
        self.port = port or os.environ.get("REPAINT_PORT", 8765)
        self.quiet = quiet
        self.connected_browsers = []

    def print(self, *args):
        if not self.quiet:
            print(*args)

    async def ws(self, websocket, path):
        async for message in websocket:
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                self.print("Expected input to be JSON:", message)
                return

            if data["type"] == BROWSER_CONNECT:
                self.connected_browsers.append(
                    RepaintBrowser(id=data["url"], websocket=websocket)
                )
                self.print(f"Browser connected: {data['url']}")

            elif data["type"] in (BROWSER_RELOAD, BROWSER_RELOAD_ASSETS):
                await self.broadcast_data(data)
            else:
                print("Unknown message type:", data["type"])

    async def broadcast_data(self, data):
        if not self.connected_browsers:
            self.print("No browsers connected")
            return

        # Send back to all connected_browsers clients
        for i, browser in enumerate(self.connected_browsers):
            try:
                await browser.send(data)
                self.print(f"Reloading browser {i+1}: {browser}")
            except websockets.ConnectionClosed:
                self.print(f"Browser {i+1} disconnected: {browser}")
                self.connected_browsers.remove(browser)

    def serve(self):
        self.print("Serving on port", self.port)
        start_server = websockets.serve(self.ws, "localhost", self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
