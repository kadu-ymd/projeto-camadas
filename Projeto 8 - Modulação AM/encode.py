from scipy.io import wavfile
import matplotlib.pyplot as plt 
import numpy as np
from utils import *

INPUT = 'music.wav'

sr, data = wavfile.read(INPUT)

SAMPLERATE = sr

n_amostras = len(data)

duration = n_amostras/sr # em segundos

t = np.linspace(0, duration, n_amostras) # em segundos

canal1 = [data[i][0] for i in range(n_amostras)]
canal2 = [data[i][1] for i in range(n_amostras)]

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


