from enlace import *
from enlaceTx import *
import time
import numpy as np
from utils import *

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
        print('recebi byte de sacrifício')
        time.sleep(.1)
        # ------------------------------------------------
        
        idle = True
        received = False
        is_full = not com1.rx.getIsEmpty()

        while idle: # ocioso
            while is_full:
                rx_head, _ = com1.getData(10)
                head = message_head(rx_head)
                received = True

            if received == True: # recebeu msg t1
                if server_id == head['h1']: # é para mim
                    idle == False # ocioso = false
            time.sleep(1) # sleep 1 sec

        received = False

        t2_message = build_message(build_head(head, b'\x02'), payload=b'')

        com1.sendData(t2_message) # envia msg t2
        time.sleep(1)

        cont = 1 # cont = 1

        while cont <= head['h3']: # cont <= numPckg
            received = False
            timer1 = time.time() # set timer1
            timer2 = time.time() # set timer2

            while is_full:
                rx_head, _ = com1.getData(10)
                head = message_head(rx_head)

                rx_payload, n_payload = com1.getData(head['h5'])
                rx_eop, _ = com1.getData(4)
                received = True
            
            if received == True: # msg t3 recebida
                pckg_status = is_package_ok(rx_head, rx_payload, rx_eop, cont)
                if pckg_status == True:
                    t4_message = build_message(build_head(head, b'\x04'), payload=rx_payload)

                    com1.sendData(t4_message) # envia msg t4
                    time.sleep(1)

                    cont += 1
                else:
                    t6_message = build_message(build_head(head, b'\x06'), payload=b'')

                    com1.sendData(t6_message) # envia msg t4
                    time.sleep(1)
            else:
                time.sleep(1)
                time_now = time.time()
                if (time_now - timer2) > 20:
                    idle = True
                    t5_message = build_message(build_head(head, b'\x05'), payload=b'')

                    com1.sendData(t5_message) # envia msg t5
                    time.sleep(1)

                    print(':-(')
                    com1.disable()
                else:
                    if (time_now - timer1) > 2:
                        t4_message = build_message(build_head(head, b'\x04'), payload=rx_payload)

                        com1.sendData(t4_message) # envia msg t4
                        time.sleep(1)

                        timer1 = time.time()    

        print('Sucesso!')

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
