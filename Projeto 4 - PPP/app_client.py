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
        tam_head = 10
        tam_payload = 114
        tam_eop = 4

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
        qtd_pacotes = math.ceil(len(txBuffer)/tam_payload)

        type1 = b'\x01' + server_id.to_bytes(1, byteorder='little') + b'\xff' + qtd_pacotes.to_bytes(1, byteorder='little') + b'\x00' + b'\xff'*5 + EOP
        while inicia == False:
            # envia t1 com identificador
            com1.sendData(type1)
            time.sleep(5)

            while (head['h1'] != server_id) and (int.from_bytes(head['h0'], byteorder="little") != 2):
                # checa se mensagem é t2 e se o id do servidor corresponde ao do arquivo utils
                rx_head, _ = com1.getData(10)
                head = message_head(rx_head)
            break
        
        print('entra na segunda etapa')
        cont = 1
        indice = 0
        while cont<=qtd_pacotes:
            if cont==qtd_pacotes-1:
                # Para o último caso, o tamanho do payload muda
                tam_payload = len(txBuffer) - qtd_pacotes*tam_payload

            payload_type3 = txBuffer[indice:cont*tam_payload]
            indice += tam_payload
            head_type3 = b'\x03' + b'\xff\xff' + qtd_pacotes.to_bytes(1, byteorder='little') + cont.to_bytes(1, byteorder='little') + tam_payload.to_bytes(1, byteorder='little') + b'\xff' + (cont-1).to_bytes(1, byteorder='little') + b'\xff'*2
            com1.sendData(head_type3+payload_type3+EOP)
            time.sleep(1)
            timer1 = time.time() # set timer1 - reenvio
            timer2 = time.time() # set timer2 - timeout

            rx_head, _ = com1.getData(10)
            head = message_head(rx_head)
            print(head['h0'])

            if head['h0'] == 4:
                # checa se a mensagem recebida é de tipo 4
                cont+=1
            
            else:
                time_now = time.time()
                if (time_now - timer1)>=5:
                    # envia o mesmo pacote com dados de tipo 3
                    com1.sendData(head_type3+payload_type3+EOP)
                    timer1 = time.time() # reset timer1 

                if (time_now - timer2)>20:
                    # envia mensagem de tipo 5
                    t5_message = build_message(build_head(head, b'\x05'), payload=b'')
                    com1.sendData(t5_message) 
                    com1.disable()

                else:
                    rx_head, _ = com1.getData(10)
                    head = message_head(rx_head)
                    while (int.from_bytes(head['h0'], byteorder="little") != 4): 
                        # while recebeu msg t4 == False:
                        rx_head, _ = com1.getData(10)
                        head = message_head(rx_head)

                        if (int.from_bytes(head['h0'], byteorder="little") == 6):
                            # Recebeu msg t6:
                            cont = head['h7'] + 1
                            com1.sendData(head_type3+payload_type3+EOP) # Envia msg t3

                            # Reset timers
                            timer1 = time.time()
                            timer2 = time.time()
                        
                    cont +=1
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()  

if __name__ == "__main__":
    main()