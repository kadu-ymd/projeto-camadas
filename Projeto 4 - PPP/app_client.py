from enlace import *
from enlaceTx import *
import time
import math

serialName = "COM3"

def main():
    try:
        print("Iniciou o main")
        com1 = enlace(serialName)
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        # Byte de sacrifício
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)
        print("Abriu a comunicação")

        inicia = False
        imageR = './img/imagem_enviada.png'
        txBuffer = open(imageR, 'rb').read()
        qtd_pacotes = math.ceil(len(txBuffer)/114).to_bytes(1, byteorder='little')

        type1 = b'\x01\x01\xff'+qtd_pacotes+b''

        # while
        if inicia == False:
            com1.sendData(type1)
            # envia t1 com identificador



        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()  

    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()