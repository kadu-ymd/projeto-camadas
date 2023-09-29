from enlace import *
from enlaceTx import *
from utils import *
import time
import math
import crcmod.predefined
from binascii import unhexlify

serialName = "COM3"

def main():
    try:
        caso = PATH_CLIENT_1
        head = dict() # Inicializa head para que ele entre no critério do while
        head['h0'] = b'\x00'
        head['h1'] = 0
        tam_payload = 114

        print("Iniciou o main")
        com1 = enlace(serialName)
        message = Message()
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        # Byte de sacrifício
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)
        print("Abriu a comunicação")

        timeout = False
        inicia = False
        imageR = './img/imagem_enviada.png'
        txBuffer = open(imageR, 'rb').read()
        qtd_pacotes = math.ceil(len(txBuffer)/tam_payload)

        head_type1 = b'\x01' + to_bytes(SERVER_ID) + BYTE1_FREE + to_bytes(qtd_pacotes) + b'\x00' + BYTE1_FREE*5
        type1 = message.build(head_type1, b'')
        
        while inicia == False:
            # envia t1 com identificador
            com1.sendData(type1)
            time.sleep(5)

            content = build_log(True, 1, len(type1), 0, qtd_pacotes, crc=0)
            file_write(caso, content, 'w')
            
            while (head['h1'] != SERVER_ID) and head['h0'] != 2:
                # checa se mensagem é t2 e se o id do servidor corresponde ao do arquivo utils
                is_full = not com1.rx.getIsEmpty()
                while is_full:
                    rx_head, _ = com1.getData(10)
                    _,_ = com1.getData(4)
                    head = message_head(rx_head)
                    break
            content = build_log(False, 2, len(rx_head)+4, '', qtd_pacotes, crc=0)
            file_write(caso, content, 'a')
            break
        
        cont = 1
        indice = 0
        while cont<=qtd_pacotes and (not timeout):
            rec = False
            if cont==qtd_pacotes:
                # Para o último caso, o tamanho do payload muda
                tam_payload = len(txBuffer) - (qtd_pacotes-1)*tam_payload
                payload_type3 = txBuffer[indice::]

            else:
                payload_type3 = txBuffer[indice:cont*tam_payload]
                print(f'payload type usa cont {cont} e vai até {cont*tam_payload} inicia com indice {indice}')

            # CRC 
            seq_str = payload_type3.hex()
            s = unhexlify(seq_str)
            crc16 = crcmod.predefined.Crc('xmodem')
            crc16.update(s)
            crc = bytes.fromhex(crc16.hexdigest())

            # --------------------------------------

            head_type3 = b'\x03' + BYTE2_FREE + to_bytes(qtd_pacotes)+ to_bytes(cont)+ to_bytes(tam_payload) + BYTE1_FREE + to_bytes(cont-1) + crc
            type3 = message.build(head_type3,payload_type3)
            com1.sendData(type3)
            time.sleep(1)

            content = build_log(True, 3, len(type3), cont, qtd_pacotes, crc)
            file_write(caso, content, 'a')

            print(f'Mensagem {cont}/{qtd_pacotes} enviada')
            print(f'CRC: {crc}')
            timer1 = time.time() # set timer1 - reenvio
            timer2 = time.time() # set timer2 - timeout

            
            cond = True
            while cond:
                is_full = not com1.rx.getIsEmpty()
                
                while is_full:
                    rx_head, _ = com1.getData(10)
                    _,_ = com1.getData(4)
                    head = message_head(rx_head)
                    rec = True
                    break
                
                    
                if head["h0"] != 4: 
                    time_now = time.time()
                    if (time_now - timer1)>5:
                        # envia o mesmo pacote com dados de tipo 3
                        print("Time out 5")
                        com1.sendData(type3)
                        time.sleep(1)
                        print(type3)

                        content = build_log(True, 3, len(type3), cont, qtd_pacotes, crc)
                        file_write(caso, content, 'a')
                        timer1 = time.time() # reset timer1 

                    if (time_now - timer2)>20:
                        # envia mensagem de tipo 5
                        print("Time out 20")
                        t5_head = b'\x05' + BYTE2_FREE + to_bytes(qtd_pacotes) + to_bytes(head['h4']) + b'\x00' + BYTE1_FREE + to_bytes(cont - 1) + BYTE2_FREE
                        t5_payload = b''
                        t5_message = message.build(t5_head, t5_payload)
                                                    
                        com1.sendData(t5_message) 
                        time.sleep(1)
                        content = build_log(True, 5, len(t5_message), cont, qtd_pacotes, crc)
                        file_write(caso, content, 'a')
                        timeout=True
                        cond=False
                        com1.disable()

                    else:   
                        #print(f'Recebi o seguinte head: {head}')
                        if rec:
                            if head['h0'] == 6:
                                content = build_log(False, 6, len(rx_head)+4, '', qtd_pacotes, crc=0)
                                file_write(caso, content, 'a')
                                        
                                cont = head['h6']
                                
                                if cont==qtd_pacotes:
                                    # Para o último caso, o tamanho do payload muda
                                    tam_payload = len(txBuffer) - (qtd_pacotes-1)*tam_payload
                                    payload_type3 = txBuffer[indice::]
                                else:
                                    payload_type3 = txBuffer[indice:cont*tam_payload]

                                # CRC 
                                seq_str = payload_type3.hex()
                                s = unhexlify(seq_str)
                                crc16 = crcmod.predefined.Crc('xmodem')
                                crc16.update(s)
                                crc = bytes.fromhex(crc16.hexdigest())
                                
                                head_type3 = b'\x03' + BYTE2_FREE + to_bytes(qtd_pacotes)+ to_bytes(cont)+ to_bytes(tam_payload) + BYTE1_FREE + to_bytes(head["h7"]) + crc

                                type3 = message.build(head_type3,payload_type3)

                                com1.sendData(type3) # Envia msg t3
                                content = build_log(True, 3, len(type3), cont, qtd_pacotes, crc)
                                file_write(caso, content, 'a')
                                        
                                time.sleep(1)

                                # Reset timers
                                timer1 = time.time()
                                timer2 = time.time()
                else:
                    if (head['h0'] == 4) and (head['h7'] == cont-1) and rec:
                        cont+=1
                        cond = False
                        indice += tam_payload
                        content = build_log(False, 4, len(rx_head)+4, cont, qtd_pacotes, crc)
                        file_write(caso, content, 'a')
                    
                print(f'timeout {timeout}')
                               
        print("Comunicação encerrada")
        com1.disable() #sucesso
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()  

if __name__ == "__main__":
    main()