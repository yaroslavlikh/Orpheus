import json
import queue
import threading

import pyttsx3
import sounddevice as sd
from websockets.sync.client import connect

from sound import speak_text
from translater import translate

SAMPLE_RATE = 16_000
SERVER_URL = "ws://127.0.0.1:8080/v1/audio/transcriptions/realtime"

audio_queue = queue.Queue()
text_queue = queue.Queue()
engine = pyttsx3.init()

ws = connect(SERVER_URL)
print(ws.recv())
ws.send(json.dumps({
    "type": "session.update",
    "session": {"sample_rate": SAMPLE_RATE, "language": "en"},
}))


def send_audio():
    while True:
        chunk = audio_queue.get()
        if chunk is None:
            ws.send(json.dumps({"type": "input_audio_buffer.commit"}))
            break
        ws.send(chunk.tobytes())


def receive_text():
    for message in ws:
        event = json.loads(message)
        if event.get("delta"):
            print(event["delta"], end="", flush=True)
        if event.get("type", "").endswith(".completed"):
            print()
            text = event.get("transcript", "")
            if text:
                text_queue.put(text)


def speak_worker():
    while True:
        text = text_queue.get()
        if text is None:
            break
        ru_text = translate(text)[0]
        print(f"[RU] {ru_text}")
        speak_text(ru_text, engine)


def callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put_nowait(indata.copy())


sender = threading.Thread(target=send_audio)
receiver = threading.Thread(target=receive_text)
speaker = threading.Thread(target=speak_worker)
sender.start()
receiver.start()
speaker.start()

with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='int16', callback=callback, blocksize=480):
    print("Начинаем запись")
    try:
        while True:
            sd.sleep(1000)
    except KeyboardInterrupt:
        pass

audio_queue.put_nowait(None)
sender.join()
receiver.join(timeout=3)
ws.close()
receiver.join()
text_queue.put(None)
speaker.join()
