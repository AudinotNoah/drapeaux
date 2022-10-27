import asyncio
import websockets

servv = "ws://141.145.193.207:443"
#servv ="ws://localhost:443"
async def hello():
    async with websockets.connect(servv) as websocket:
        await websocket.send("Hello world!")
        msg = await websocket.recv()
        print(str(msg))

asyncio.run(hello())