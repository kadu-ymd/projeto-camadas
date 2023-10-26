import numpy as np

def todB(s):
    # Transforma intensidade acustica em dB
    sdB = 10 * np.log10(s)
    return sdB