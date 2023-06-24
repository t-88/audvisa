import numpy as np
import wave

file_name = "sounds/are-you-sure-about-that.wav"

file = wave.open(file_name,"rb")
freq =  file.getframerate()
frames = file.getnframes()

k = 5
while k:
    k = file.readframes(1)
    print(np.frombuffer(k,dtype=np.int16))

