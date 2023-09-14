from enlace import *
from enlaceTx import *
import time
import numpy as np

serialName = "COM5"
STD_HEAD = b'\xff'*12
STD_EOP = b'\xee'*3
MSG_NEXT = STD_HEAD + STD_EOP
MSG_END = STD_HEAD + b'\xA0' + STD_EOP

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
        handshake = STD_HEAD + STD_EOP
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
        
        cond1, cond2 = False, False
        
        # loop
        index_cond = int(rx_head[0]) # começa no 1
        print(index_cond)
        img_list = [rx_payload]
        
        com1.sendData(MSG_NEXT)
        time.sleep(1)

        for i in range(1, total_pck):
            print('começo loop')
            rx_head, _ = com1.getData(12)
            
            pck_index = rx_head[0]
            payload_size = rx_head[1]
            total_pck = int(rx_head[2])

            rx_payload, _ = com1.getData(payload_size)

            rx_eop, _ = com1.getData(3) # EOP

            # verifica o índice
            if (index_cond + 1) == pck_index:
                index_cond += 1
                cond1 = True

            # verifica se o pacote chegou completo
            if rx_eop == (b'\xEE'*3):
                cond2 = True

            # faz um booleano das duas condições necessárias para continuar o código
            if (cond1 and cond2):
                img_list.append(rx_payload)
                com1.sendData(MSG_NEXT)
                time.sleep(1)
            else:
                print('Ops! Algo deu errado.')
                
            if pck_index == total_pck:
                for pck in img_list:
                    image_bytes += pck

        com1.sendData(MSG_END)
        time.sleep(3)

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
