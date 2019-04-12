from __future__ import division
import asyncio
import websockets
import json
import pyaudio
from google.cloud.speech import enums

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = int(RATE / 10)

audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)


# async def microphone_client():
#     async with websockets.connect(
#             'ws://0.0.0.0:8000/') as websocket:
#         await websocket.send(json.dumps({
#             'rate': RATE,
#             'format': enums.RecognitionConfig.AudioEncoding.LINEAR16,
#             'language': 'en-US'
#         }))
#         while True:
#             data = stream.read(CHUNK)
#             await websocket.send(data)

config = {
    'user_id': '5c7e08bafc6ccfe86aa58193',
    'document_id': '5c9ddfa347acbdc0668fe3e6',
    'chunk_id': '5c9ddfad47acbdae038fe3e7'
}


# 13.234.92.107:5001/score
async def microphone_client():
    async with websockets.connect(
            'ws://0.0.0.0:8000/') as websocket:
        await websocket.send(json.dumps(config))
        while True:
            try:
                data = stream.read(CHUNK)
                print(data)
                await websocket.send(data)
            except KeyboardInterrupt:
                print('Bye')
                await websocket.send('stop')
                break
        data = await websocket.recv()
        print(data)
asyncio.get_event_loop().run_until_complete(microphone_client())
