import websockets
import json
from time import sleep
import asyncio

async def listen():
    url = "ws://127.0.0.1:8000"

    async with websockets.connect(url) as ws:
        while True:
            msg = { "method": "state", "value": "ready"}
            await ws.send(json.dumps(msg))
            print("sent")
            sleep(1)


asyncio.get_event_loop().run_until_complete(listen())