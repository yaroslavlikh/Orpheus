import sounddevice as sd
import queue
import threading
import numpy as np 

q = queue.Queue()

def maximum_sound(audio_queue):
    while True:
        chunk = audio_queue.get()
        if chunk is None:
            break
        print(np.abs(chunk).max())

thread = threading.Thread(target=maximum_sound, args=(q,))
thread.start()

def callback(indata, frames, time, status):
    q.put_nowait(indata.copy())
    if status:
        print(status)

with sd.InputStream(samplerate=16000, channels=1, dtype='float32', callback=callback, blocksize=480):
    sd.sleep(10000)
    q.put_nowait(None)
    thread.join()