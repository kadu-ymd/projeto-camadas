from enlace import *
from enlaceTx import *
import time
import numpy as np

serialName = "COM5"

def main():
    try:
        print("Iniciou o main")
        com1 = enlace(serialName)

        # ------------------------------------------------
        # Byte de sacrifício (oferenda)
        com1.enable()
        print("esperando 1 byte de sacrifício")
        _, _ = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)
        # ------------------------------------------------
    
        # ------------------------------------------------
        # Handshake
        handshake = b'\xff'*12 + b'\xee'*3
        rx_handshake, n_Hs = com1.getData(15)

        if rx_handshake == handshake:
            com1.sendData(handshake)
            time.sleep(1)

        imageW = './img/r_image.png'

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
