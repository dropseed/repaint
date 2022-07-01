import asyncio
import json
import os

import websockets


class Server:
    def __init__(self, port=8765, quiet=False):
        self.port = port
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

            if data["type"] == "browser-connect":
                self.connected_browsers.append(websocket)
                websocket._repaint_id = data["url"]
                self.print(f"Browser connected: {data['url']}")

            elif data["type"] == "reload":
                if not self.connected_browsers:
                    self.print("No browsers connected")
                    return

                # Send back to all connected_browsers clients
                for i, browser_ws in enumerate(self.connected_browsers):
                    try:
                        await browser_ws.send(json.dumps({"type": "browser-reload"}))
                        self.print(f"Reloading browser {i+1}: {browser_ws._repaint_id}")
                    except websockets.ConnectionClosed:
                        self.connected_browsers.remove(browser_ws)

            else:
                print("Unknown message type:", data["type"])

    def serve(self):
        start_server = websockets.serve(self.ws, "localhost", self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
