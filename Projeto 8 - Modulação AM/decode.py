from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
from utils import *
import sounddevice as sd

FREQ_C = 14000
sr, data = wavfile.read("am-music.wav")
print(data)

n_amostras = len(data)

duration = n_amostras / sr  # em segundos

t = np.linspace(0, duration, n_amostras)  # em segundos

plt.figure()
plt.plot(t, data)
plt.grid(True)
plt.title('Dado na música')

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

signalMeu().plotFFT(filtrado, sr)

plt.show()

sd.play(filtrado, sr)
sd.wait()