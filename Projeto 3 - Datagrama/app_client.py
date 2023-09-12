#####################################################
# Camada Física da Computação

from enlace import *
from enlaceTx import *
import time
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# use uma das 3 opcoes para atribuir à variável a porta usada
# serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
# serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)

meio = False
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

        if meio:
            head = b'\xff'*12
            payload = b'\xbb'*50
            eop = b'\xee'*3

        pacote = head+payload+eop
        com1.sendData(pacote)
        time.sleep(1)

        t_inicio = time.time()
        delta_t = 0
        while delta_t <5 and com1.rx.getIsEmpty():
            t_atual = time.time()
            delta_t = t_atual-t_inicio
            print(f'delta t = {delta_t} e t_atual {t_atual} e t_inicio {t_inicio}')
            
        if delta_t>=5:
            reenvio = input("Servidor inativo. Tentar novamente? S/N")
        else:
            rx_handshake, _ = com1.getData(15)

        
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