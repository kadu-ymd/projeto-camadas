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

        # primeiro ciclo

        image_bytes = b''
        imageW = 'Projeto 3 - Datagrama/img/img_recebida.png'
        
        rx_head, _ = com1.getData(12)

        _ = rx_head[0]
        payload_size = rx_head[1]
        total_pck = int(rx_head[2])

        rx_payload, _ = com1.getData(payload_size)

        _, _ = com1.getData(3)
        image_bytes += rx_payload

        print(image_bytes)

        # loop
        for i in range(1, total_pck):
            rx_head, _ = com1.getData(12)

            pck_index = rx_head[0]
            print(pck_index)
            payload_size = rx_head[1]
            total_pck = int(rx_head[2])

            rx_payload, _ = com1.getData(payload_size)

            _, _ = com1.getData(3) # EOP
            image_bytes += rx_payload

        print(image_bytes)
        with open(imageW, 'wb') as file:
            file.write(image_bytes)
        
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
