from enlace import *
from enlaceTx import *
from utils import *
import time
import math

serialName = "COM4"

def main():
    try:
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

            while (head['h1'] != SERVER_ID) and head['h0'] != 2:
                # checa se mensagem é t2 e se o id do servidor corresponde ao do arquivo utils
                is_full = not com1.rx.getIsEmpty()
                while is_full:
                    rx_head, _ = com1.getData(10)
                    _,_ = com1.getData(4)
                    head = message_head(rx_head)
                    break
            break
        
        cont = 1
        indice = 0
        while cont<=qtd_pacotes:
            rec = False
            if cont==qtd_pacotes:
                # Para o último caso, o tamanho do payload muda
                tam_payload = len(txBuffer) - (qtd_pacotes-1)*tam_payload
                payload_type3 = txBuffer[indice::]

            else:
                payload_type3 = txBuffer[indice:cont*tam_payload]
            head_type3 = b'\x03' + BYTE2_FREE + to_bytes(qtd_pacotes)+ to_bytes(cont)+ to_bytes(tam_payload) + BYTE1_FREE + to_bytes(cont-1) + BYTE2_FREE
            type3 = message.build(head_type3,payload_type3)
            com1.sendData(type3)
            time.sleep(1)
            print(f'Mensagem {cont}/{qtd_pacotes} enviada')
            timer1 = time.time() # set timer1 - reenvio
            timer2 = time.time() # set timer2 - timeout

            is_full = not com1.rx.getIsEmpty()
            while is_full:
                rx_head, _ = com1.getData(10)
                _,_ = com1.getData(4)
                head = message_head(rx_head)
                rec = True
                break

            if (head['h0'] == 4) and (head['h7'] == cont-1) and rec:
                # checa se a mensagem recebida é de tipo 4
                indice += tam_payload
                cont+=1
            else:
                time_now = time.time()
                if (time_now - timer1)>5:
                    # envia o mesmo pacote com dados de tipo 3
                    print("Time out 5")
                    com1.sendData(type3)
                    time.sleep(1)
                    print(type3)
                    timer1 = time.time() # reset timer1 

                if (time_now - timer2)>20:
                    # envia mensagem de tipo 5
                    print("Time out 20")
                    t5_head = b'\x05' + BYTE2_FREE + to_bytes(qtd_pacotes) + to_bytes(head['h4']) + b'\x00' + BYTE1_FREE + to_bytes(cont - 1) + BYTE2_FREE
                    t5_payload = b''
                    t5_message = message.build(t5_head, t5_payload)
                                               
                    #t5_message = message.build(build_head(head, b'\x05'), payload=b'')
                    com1.sendData(t5_message) 
                    time.sleep(1)
                    print(f"t5 é {t5_message}")
                    com1.disable()

                else:
                    rec = False
                    is_full = not com1.rx.getIsEmpty()
                    while is_full:
                        rx_head, _ = com1.getData(10)
                        _,_ = com1.getData(4)
                        head = message_head(rx_head)
                        rec = True
                        break
                    
                    print(head)
                    while head['h0'] != 4: 
                        # while recebeu msg t4 == False:
                        is_full = not com1.rx.getIsEmpty()
                        while is_full:
                            rx_head, _ = com1.getData(10)
                            _,_ = com1.getData(4)
                            head = message_head(rx_head)
                            break
                        print(f'ho é {head["h0"]}')
                        if head['h0'] == 6:
                            # Recebeu msg t6:
                            
                            cont = head['h7'] + 1
                            head_type3 = b'\x03' + BYTE2_FREE + to_bytes(qtd_pacotes)+ to_bytes(cont)+ to_bytes(tam_payload) + BYTE1_FREE + to_bytes(cont-1) + BYTE2_FREE
                            if cont==qtd_pacotes-1:
                                # Para o último caso, o tamanho do payload muda
                                tam_payload = len(txBuffer) - (qtd_pacotes-1)*tam_payload
                                payload_type3 = txBuffer[indice::]
                            else:
                                payload_type3 = txBuffer[indice:cont*tam_payload]
                                print(payload_type3)
            
                            
                            type3 = message.build(head_type3,payload_type3)
                            print(f'envio t3 = {type3} e tam_payload = {tam_payload} e indice {indice}')

                            com1.sendData(type3) # Envia msg t3
                            
                            time.sleep(1)

                            # Reset timers
                            timer1 = time.time()
                            timer2 = time.time()
                        
        print("Comunicação encerrada")
        com1.disable() #sucesso
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()  

if __name__ == "__main__":
    main()