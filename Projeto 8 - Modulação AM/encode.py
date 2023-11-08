from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
from utils import *
import sounddevice as sd

INPUT = "music.wav"
FREQ_C = 14000

signal = signalMeu()

sr, data = wavfile.read(INPUT)

SAMPLERATE = sr

n_amostras = len(data)

duration = n_amostras / sr  # em segundos

t = np.linspace(0, duration, n_amostras)  # em segundos

canal1 = [data[i][0] for i in range(n_amostras)]
canal1 /= (np.max(np.abs(canal1)))

a = 0.01134
b = 0.0102
c = 1
d = -1.706
e = 0.728

y1 = [0, 0]

for k in range(2, len(canal1)):
    y1.append(-d * y1[k - 1] - e * y1[k - 2] + a * canal1[k - 1] + b * canal1[k - 2])

c_t = np.sin(2 * np.pi * FREQ_C * t)
s_t = [y1[i] * c_t[i] for i in range(len(t))]

wavfile.write("am-music.wav", SAMPLERATE, np.asarray(s_t))

# ____________________________________________________

# Áudios

## Normalizado

# sd.play(canal1, SAMPLERATE)
# sd.wait()

## Filtrado

# sd.play(y1, SAMPLERATE)
# sd.wait()

# ____________________________________________________

# Gráficos

plt.figure()
plt.plot(t, canal1)
plt.grid(True)
plt.title('Áudio normalizado')

plt.figure(figsize=(8, 8))
plt.subplot(221)
plt.plot(t, y1, 'purple')
plt.grid(True)
plt.title('Áudio filtrado (domínio do tempo)')

plt.subplot(222)
frequency, amplitude = signal.calcFFT(y1, SAMPLERATE)
plt.plot(frequency, np.abs(amplitude), 'purple')
plt.grid(True)
plt.title('Áudio filtrado (domínio do frequência)')

plt.subplot(223)
plt.plot(t, s_t, 'lightgreen')
plt.grid(True)
plt.title('Áudio modulado (domínio do tempo)')

plt.subplot(224)
frequency, amplitude = signal.calcFFT(s_t, SAMPLERATE)
plt.plot(frequency, np.abs(amplitude), 'lightgreen')
plt.grid(True)
plt.title('Áudio modulado (domínio do frequência)')

plt.show()

# ____________________________________________________