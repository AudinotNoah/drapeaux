import asyncio
import websockets

#tuer le process
#sudo lsof -i :443
#sudo kill -9

async def echo(websocket,test):
    async for message in websocket:
        await websocket.send(message)

async def main():
    async with websockets.serve(echo, "", 443):
        await asyncio.Future()  # run forever

#asyncio.run(main())
loop = asyncio.get_event_loop()
result = loop.run_until_complete(main())