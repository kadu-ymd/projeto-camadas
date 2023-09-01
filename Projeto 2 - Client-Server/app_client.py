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
dicio_binario = {1:'0001', 2:'0010', 3:'0011', 4:'0100'}

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
        txBuffer = to_bytearray(n) # Todos os comandos escolhidos

        #com1.sendData(bytes((len(txBuffer),)))
        #time.sleep(1)  

        j = 0
        while j < len(txBuffer):
            i = 1
            while i<=3:
                segundo_comando = txBuffer[i+1]
                primeiro_comando = txBuffer[i]
                # Soma das strings
                strings = dicio_binario[len(primeiro_comando)] + dicio_binario[len(segundo_comando)]
                print(f'O próximo comando é {hex(strings)}')
                com1.sendData(bytes(hex(int(strings,2))))
                time.sleep(1)
                com1.sendData(bytes(primeiro_comando,)+bytes((segundo_comando,)))
                time.sleep(1)
                
                i+=2
            j+=2

        print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
               
        #com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
        #time.sleep(1)

        n_rx, _ = com1.getData(1)
        if n_rx == b'\xCC':
            print("Timeout!")
            com1.disable()

        recebidos = int.from_bytes(n_rx, byteorder='little')

        if recebidos==n:
            print("Todos os bytes foram recebidos")
            print(f'enviei {n} comandos e o seguintes conteudos: {np.asarray(txBuffer)}')

        else:
            print("Faltam bytes a serem recebidos.")

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