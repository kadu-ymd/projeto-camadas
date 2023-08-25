#####################################################
# Camada Física da Computação

from enlace import *
from enlaceTx import *
from cliente import *
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
comandos = ["\x00\x00\x00\x00", "\x00\x00\xBB\x00", "\xBB\x00\x00", "\x00\xBB\x00", "\x00\x00\xBB", "\x00\xAA", "\xBB\x00", "\x00", "\xBB"]


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

        n = sorteia_numero()
        txBuffer = to_bytearray(n)

        com1.sendData(bytes((len(txBuffer),)))
        time.sleep(1)

        print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
               
        com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
        time.sleep(1)
        n_rx, _ = com1.getData(1)
        recebidos = int.from_bytes(n_rx, byteorder='little')
        print(f'O servidor recebeu {recebidos} comandos')

        if recebidos==n:
            print("Todos os bytes foram recebidos")
            print(f'enviei {n} comandos e o seguintes conteudos: {np.asarray(txBuffer)}')

        else:
            print("Faltam bytes serem recebidos")

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