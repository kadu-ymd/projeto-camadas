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
canal2 = [data[i][1] for i in range(n_amostras)]

# Música original
# sd.play(canal1, SAMPLERATE)
# sd.wait()

# --------------------------------------

# Descomentar para visualizar o audio

# plt.figure()
# plt.plot(t, canal1)
# plt.grid(True)
# plt.title('Canal 1')

# plt.figure()
# plt.plot(t, canal2)
# plt.grid(True)
# plt.title('Canal 2')

# plt.show()

# --------------------------------------

a = 0.01134
b = 0.0102
c = 1
d = -1.706
e = 0.728

y1 = [0, 0]

for k in range(2, len(canal1)):
    y1.append(-d * y1[k - 1] - e * y1[k - 2] + a * canal1[k - 1] + b * canal1[k - 2])

# signal.plotFFT(canal1, SAMPLERATE)
# plt.title('Sem filtro')

signal.plotFFT(y1, SAMPLERATE)
plt.title('Com filtro')

c_t = np.sin(2 * np.pi * FREQ_C * t)
s_t = [y1[i] * c_t[i] for i in range(len(t))]

signal.plotFFT(s_t, SAMPLERATE)
plt.title('Modulado com filtro')

wavfile.write("am-music.wav", SAMPLERATE, np.asarray(s_t))

# Música original
# sd.play(y1, SAMPLERATE)
# sd.wait()



# --------------------------------------

# Descomentar para visualizar o audio filtrado

# plt.figure()
# plt.plot(t, y1)
# plt.plot(t, canal1)
# plt.grid(True)
# plt.title('Áudio do canal 1 filtrado')

# plt.figure()
# plt.plot(t, canal2)
# plt.grid(True)
# plt.title('Canal 2')

plt.show()

# --------------------------------------