import sounddevice as sd
import numpy as np

threshold = 80
clap = False

def detectClap(indata, frames, time, status):
    global clap
    volume_norm = np.linalg.norm(indata) * 10
    if volume_norm > threshold:
        print("Clapped!")
        clap = True

def listenForClap():
    with sd.InputStream(callback=detectClap):
        return sd.sleep(1000)
    

def mainClapExe():
    while True:
        listenForClap()
        if clap == True:
            break
        else:
            pass