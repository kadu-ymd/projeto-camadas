from enlace import *
from enlaceTx import *
import time
import numpy as np
from utils import *
import crcmod.predefined
from binascii import unhexlify

serialName = "COM5"
IMAGE_W = 'Projeto 4 - PPP/img/img_recebida.png'

def main():
    try:
        print("Iniciou o main")
        com1 = enlace(serialName)
        message = Message()
        
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
        byte_image = list()

        while idle: # ocioso
            is_full = not com1.rx.getIsEmpty()
            while is_full:
                rx_head, n_head = com1.getData(10)
                head = message.head_unpack(rx_head)
                QTD_PACOTES = head['h3']
                n_pck = head['h4']
                
                _, n_eop = com1.getData(4)
                received = True
                break
            if received == True: # recebeu msg t1
                if SERVER_ID == head['h1']: # é para mim
                    idle = False # ocioso = false
                    log = build_log(False, 1, QTD_PACOTES, (n_head + n_eop), n_pck, crc='')
                    file_write(PATH_SERVER_1, log, 'w')
            time.sleep(1) # sleep 1 sec

        received = False

        t2_head = b'\x02' + BYTE2_FREE + to_bytes(QTD_PACOTES) + to_bytes(n_pck) + b'\x00' + b'\xff' + to_bytes(head['h7']) + BYTE2_FREE
        t2_payload = b''

        t2_message = message.build(t2_head, t2_payload)

        com1.sendData(t2_message) # envia msg t2
        time.sleep(.2)

        log = build_log(True, 2, QTD_PACOTES, (len(t2_head) + len(t2_payload) + 4), n_pck, crc='')
        f = open(PATH_SERVER_1, 'a', encoding=ENCODING)
        f.write(log)
        f.close()

        cont = 1 # cont = 1
        timeout = False
        reset1 = True
        reset2 = True

        while cont <= head['h3'] and not(timeout): # cont <= numPckg
            is_full = not com1.rx.getIsEmpty()
            received = False

            if reset1:
                timer1 = time.time() # set timer1
            if reset2:
                timer2 = time.time() # set timer2
            
            print(YELLOW + 'Estou tentando receber algo...')
            while is_full:
                rx_head, n_head = com1.getData(10)
                head = message_head(rx_head)
                n_pck = head['h4']
                payload_size = head['h5']
                
                rx_crc = to_bytes(head['h8']) + to_bytes(head['h9'])

                rx_payload, _ = com1.getData(payload_size)

                _,_ = com1.getData(4)
                received = True

                crc = message.crc_build(rx_payload)
                crc_log = crc
                crc = bytes.fromhex(crc)
                
                break
            
            if received == True: # msg t3 recebida
                log = build_log(False, 3, QTD_PACOTES, (n_head + payload_size + 4), n_pck, crc_log)
                f = open(PATH_SERVER_1, 'a', encoding=ENCODING)
                f.write(log)
                f.close()

                # Vai resetar os timers
                reset1 = True
                reset2 = True
                
                pckg_status = is_package_ok(rx_head, cont, rx_crc, crc)
                if (pckg_status == True) and (head['h0'] == 3): # pckg ok
                    print(GREEN + 'Recebi uma mensagem do tipo 3 e o pacote está OK!')
                    t4_head = b'\x04' + BYTE2_FREE + to_bytes(QTD_PACOTES) + to_bytes(n_pck) + b'\x00' + BYTE1_FREE + to_bytes(cont - 1) + BYTE2_FREE
                    t4_payload = b''

                    t4_message = message.build(t4_head, t4_payload)

                    com1.sendData(t4_message) # envia msg t4
                    time.sleep(.2)

                    byte_image.append(rx_payload)

                    cont += 1

                    log = build_log(True, 4, QTD_PACOTES, (len(t4_head) + len(t4_payload) + 4), n_pck, crc_log)
                    f = open(PATH_SERVER_1, 'a', encoding=ENCODING)
                    f.write(log)
                    f.close()
                else:
                    print(RED + 'Recebi uma mensagem do tipo 3 mas o pacote não está OK!')
                    t6_head = b'\x06' + BYTE2_FREE + to_bytes(QTD_PACOTES) + to_bytes(n_pck) + b'\x00' + to_bytes(cont) + to_bytes(cont - 1) + BYTE2_FREE
                    t6_payload = b''
                    t6_message = message.build(t6_head, t6_payload)

                    com1.sendData(t6_message) # envia msg t6
                    time.sleep(.2)

                    log = build_log(True, 6, QTD_PACOTES, (len(t6_head) + len(t6_payload) + 4), n_pck, crc_log)
                    f = open(PATH_SERVER_1, 'a', encoding=ENCODING)
                    f.write(log)
                    f.close()

                    com1.rx.clearBuffer()
            else:
                print(RED + 'Não recebi mensagens!')

                # Não vai resetar os timers
                reset1 = False
                reset2 = False

                time.sleep(1)
                time_now = time.time()
                if (time_now - timer2) > 20:
                    idle = True # ocioso = True
                    t5_head = b'\x05' + BYTE2_FREE + to_bytes(QTD_PACOTES) + to_bytes(n_pck) + b'\x00' + BYTE1_FREE + to_bytes(cont - 1) + BYTE2_FREE
                    t5_payload = b''

                    t5_message = message.build(t5_head, t5_payload)

                    com1.sendData(t5_message) # envia msg t5
                    time.sleep(.2)

                    log = build_log(True, 5, QTD_PACOTES, (len(t5_head) + len(t5_payload) + 4), n_pck, '')
                    f = open(PATH_SERVER_1, 'a', encoding=ENCODING)
                    f.write(log)
                    f.close()
                    
                    timeout = True
                    print('Timeout :(')
                    com1.disable() # encerra COM
                
                if (time_now - timer1) > 2:
                    print(YELLOW + 'Tentando comunicação com client...')
                    t4_head = b'\x04' + BYTE2_FREE + to_bytes(QTD_PACOTES) + to_bytes(n_pck) + b'\x00' + to_bytes(head['h7']) + to_bytes(cont - 1) + BYTE2_FREE
                    t4_payload = b''

                    t4_message = message.build(t4_head, t4_payload)

                    com1.sendData(t4_message) # envia msg t4
                    time.sleep(.2)

                    log = build_log(True, 4, QTD_PACOTES, (len(t4_head) + len(t4_payload) + 4), n_pck, '')
                    f = open(PATH_SERVER_1, 'a', encoding=ENCODING)
                    f.write(log)
                    f.close()
                    timer1 = time.time()

        image = list_to_bytearray(byte_image)

        with open(IMAGE_W, 'wb') as file:
            file.write(image),

        print(GREEN + 'Sucesso!')
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
