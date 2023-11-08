from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
from utils import *
import sounddevice as sd

FREQ_C = 14000

signal = signalMeu()

sr, data = wavfile.read("am-music.wav")

SAMPLERATE = sr

n_amostras = len(data)

duration = n_amostras / sr  # em segundos

t = np.linspace(0, duration, n_amostras)  # em segundos

c_t = np.sin(2 * np.pi * FREQ_C * t)
m_t = [data[i] * c_t[i] for i in range(len(t))]

filtrado = [0, 0]
a = 0.01134
b = 0.0102
c = 1
d = -1.706
e = 0.728

for k in range(2, len(m_t)):
    filtrado.append(-d * filtrado[k - 1] - e * filtrado[k - 2] + a * m_t[k - 1] + b * m_t[k - 2])

# ____________________________________________________

# Áudios

## Demodulado e filtrado

sd.play(filtrado, SAMPLERATE)
sd.wait()

# ____________________________________________________

# Gráficos

plt.figure(figsize=(10, 4))

plt.subplot(121)
plt.plot(t, m_t, 'orange')
plt.grid(True)
plt.title("Sinal demodulado (domínio do tempo)")

plt.subplot(122)
frequency1, amplitude1 = signal.calcFFT(m_t, SAMPLERATE)
plt.plot(frequency1, np.abs(amplitude1), 'orange')
plt.grid(True)
plt.title("Sinal demodulado (domínio da frequência)")

plt.figure()
frequency2, amplitude2 = signal.calcFFT(filtrado, SAMPLERATE)
plt.plot(frequency2, np.abs(amplitude2), 'gold')
plt.grid(True)
plt.title("Sinal demodulado e filtrado (domínio da frequência)")

plt.show()

# ____________________________________________________