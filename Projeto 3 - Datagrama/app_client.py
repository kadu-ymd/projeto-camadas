#####################################################
# Camada Física da Computação

from enlace import *
from enlaceTx import *
import time
import math

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# use uma das 3 opcoes para atribuir à variável a porta usada
# serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
# serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)

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

        # Handshake
        head = b'\xff'*12
        payload = b''
        eop = b'\xee'*3

        pacote = head+payload+eop
        com1.sendData(pacote)
        time.sleep(1)

        while com1.rx.getIsEmpty():
            t_inicio = time.time()
            delta_t = 0
            while delta_t <5 and com1.rx.getIsEmpty():
                t_atual = time.time()
                delta_t = t_atual-t_inicio
                print(f'Tempo = {delta_t:.2f} segundos', end='\r')
                
            if delta_t>=5:
                reenvio = input("Servidor inativo. Tentar novamente? S/N ")
                if reenvio == "N":
                    com1.disable()
                    raise Exception("Não será reenviado")
                #_,_ = com1.getData(1)

            else:
                rx_handshake, _ = com1.getData(15)

        imageR = './img/imagem_enviada.png'
        txBuffer = open(imageR, 'rb').read()
        qtd_pacotes = math.ceil(len(txBuffer)/50)

        cont = 0
        for i in range(1, qtd_pacotes):
            payload = txBuffer[cont:i*50]

            #pck_index = (i+1).to_bytes(1, byteorder='little') # envio do indice errado
            pck_index = (i).to_bytes(1, byteorder='little')
            pck_size = len(payload).to_bytes(1, byteorder='little')
            qt_pck = qtd_pacotes.to_bytes(1, byteorder='little')
            head = pck_index + pck_size + qt_pck + b'\xff'*9

            cont+=50
            pacote = head+payload+eop
            com1.sendData(pacote)
            time.sleep(1)

            rx_next, _ = com1.getData(15)
            print('Recebi a confirmação de que o server recebeu', pck_index)
        
        # Demais arquivos, como é float
        payload = txBuffer[cont::]
        pck_index = (i+1).to_bytes(1, byteorder='little')
        #pck_size = (len(payload)+1).to_bytes(1, byteorder='little') # payload com o tamanho errado
        pck_size = len(payload).to_bytes(1, byteorder='little')
        qt_pck = qtd_pacotes.to_bytes(1, byteorder='little')
        head = pck_index + pck_size + qt_pck + b'\xff'*9
        pacote = head+payload+eop
        com1.sendData(pacote)
        time.sleep(1)

        _,_ = com1.getData(16)
        print('A mensagem foi recebida')


        com1.disable()
        
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.


        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()  

    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()