import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import IPython
import binascii
from scipy.io import wavfile

def toBin(text):
    return list(int(b) for b in bin(int.from_bytes(text.encode(), 'big'))[2:])

def toStr(arr):
    i = int("".join(str(c) for c in arr), 2)
    return i.to_bytes((i.bit_length() + 7) // 8, 'big').decode()

text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut eros augue, tincidunt mollis urna at, molestie malesuada elit."
assert toStr(toBin(text)) == text
bintext = toBin(text)

step = 100
amplitude = 20000
h = np.multiply(np.ones(step), amplitude)

def matcher(signal, h, step, decision):
    matched = np.convolve(signal, h[::-1])
    sampled = matched[np.arange(0, len(matched), step)]
    return [decision(s) for s in sampled]

recRate, rec = wavfile.read("output2.wav")
print("noise rate", recRate)

dec = matcher(rec[15000:], h, step, lambda x: 0 if x > 0 else 1)

dec2 = [1-x for x in dec]

print(bintext)
print(dec)
print(dec2)

for i in range(0, len(dec) - 100):
    if dec[i] != bintext[i]:
        print(dec[i], "was not", bintext[i])

print(toStr(dec[:-1]))
print(text)


