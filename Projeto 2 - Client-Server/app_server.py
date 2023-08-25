from enlace import *
from enlaceTx import *
from cliente import *
import time
import numpy as np

serialName = "COM5"

def main():
    try:
        print("Iniciou o main")
        com1 = enlace(serialName)
    
        com1.enable()
        print("esperando 1 byte de sacrifício")
        _, _ = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)
    
        n, _ = com1.getData(1)
        n_bytes = int.from_bytes(n, byteorder='little')

        print(com1.getData(n_bytes))

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
