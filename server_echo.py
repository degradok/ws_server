import websockets
import json
import asyncio

WEB_PORT = 8000
SWIM_PORT = 8800


class WebPage:
    port = 5432
    is_ready = False 
    mode = "manual"

    def __init__(self, port):
        self.port = port

    async def connection(self, websocket, path):
        # print("A client just connected")
        await self.handler(websocket)

    async def handler(self, websocket):
        while True:
            buffer = await websocket.recv()
            await self.process(buffer)

    async def process(self, buffer):
        self.msg = json.loads(buffer)
        # print(self.buffe)
        # print(msg)
        if self.msg["method"] == "state" or self.msg["method"] == "mode" or self.msg["method"] == "stop":
            await self.general_msg()
        elif self.msg["method"] == "move":
            await self.manual_msg()
        elif self.msg["method"] == "pool_dimensions" or self.msg["method"] == "start" or self.msg["method"] == "velocity" or self.msg["method"] == "shit_dimensions":
            await self.auto_msg()


    async def general_msg(self):
        if self.msg["method"] == "state":
            self.is_ready = self.msg["value"]
        elif self.msg["method"] == "mode":
            self.mode = self.msg["mode"]
        elif self.msg["method"] == "stop":
            pass



    async def manual_msg(self):
        pass


    async def auto_msg(self):
        if self.msg["method"] == "pool_dimensions":
            self.length = self.msg["length"]
            self.width = self["width"]
        elif self.msg["method"] == "start":
            pass
        elif self.msg["method"] == "velocity":
            self.velocity = self.msg["value"]
        elif self.msg["method"] == "shit_dimensions":
            self.length = self.msg["length"]
            self.width = self["width"]
        


class SwimShit:
    port = 5431
    is_ready = False 
    buffer = ""

    def __init__(self, port):
        self.port = port

    async def connection(self, websocket, path):
        # print("A client just connected")
        await self.handler(websocket)

    async def handler(self, websocket):
        while True:
            self.buffer = await websocket.recv()
            await self.process()

    async def process(self):
        msg = json.loads(self.buffer)
        # print(self.buffer)
        # print(msg)
        if msg["method"] == "state":
            if msg["value"] == "ready":
                self.is_ready = True



swimshit = SwimShit(SWIM_PORT)
webpage = WebPage(WEB_PORT)
swim_server = websockets.serve(webpage.connection, "localhost", swimshit.port)
webpage_server = websockets.serve(webpage.connection, "localhost", webpage.port)

asyncio.get_event_loop().run_until_complete(webpage_server)
asyncio.get_event_loop().run_until_complete(swim_server)
asyncio.get_event_loop().run_forever()