from datetime import datetime
import crcmod.predefined
from binascii import unhexlify

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = '\033[33m'

EOP = b'\xAA\xBB\xCC\xDD'
SERVER_ID = 1
BYTE1_FREE = b'\xff'
BYTE2_FREE = b'\xff\xff'

ENCODING = 'utf-8'

PATH_CLIENT_1 = './logs/Client1.txt'
PATH_CLIENT_2 = './logs/Client2.txt'
PATH_CLIENT_3 = './logs/Client3.txt'
PATH_CLIENT_4 = './logs/Client4.txt'

PATH_SERVER_1 = 'Projeto 4 - PPP/logs/Server1.txt'
PATH_SERVER_2 = 'Projeto 4 - PPP/logs/Server2.txt'
PATH_SERVER_3 = 'Projeto 4 - PPP/logs/Server3.txt'
PATH_SERVER_4 = 'Projeto 4 - PPP/logs/Server4.txt'

def message_head(rx_head: bytearray):
    try:
        head = {'h0': rx_head[0], 'h1': rx_head[1],
                'h2': rx_head[2], 'h3': rx_head[3],
                'h4': rx_head[4], 'h5': rx_head[5],
                'h6': rx_head[6], 'h7': rx_head[7],
                'h8': rx_head[8], 'h9': rx_head[9]}
        return head
    
    except (TypeError, IndexError) as error:
        print(error)

def to_bytes(i: int):
    try:
        return (i).to_bytes(1, byteorder='little')
    except TypeError as error:
        print(error)

def build_head(head: dict, msg_type: bytes, message: bytearray = b''):
    try:
        for i in head.values():
            message += to_bytes(i)
        return message
    except TypeError as error:
        print(error)

def build_message(built_head: bytearray, payload: bytearray, eop: bytearray = EOP):
    return built_head + payload + eop

def is_package_ok(rx_head: bytearray, cont: int, crc1, crc2):
    last_pckg = message_head(rx_head)['h7']
    return (((cont - 1) == last_pckg) and (crc1 == crc2))

def list_to_bytearray(list: list):
    array: bytearray = b''
    for i in list:
        array += i
    return array

def get_date():
    '''
    Retorna a data no formato dd/mm/aa.
    '''
    return str(datetime.now().strftime("%d/%m/%y"))

def get_time():
    '''
    Retorna o horário no formato hora:mês:seg.ms.
    '''
    return str(datetime.now().strftime("%H:%M:%S.%f"))

def build_log(tx: bool, type: int, pck_total: int, pck_len: int, n_pck: int, crc, date: str = get_date(), time: str = get_time(), sep: str = ' │ '): 
    '''
    Constói o log no formato 'DATA HORA │ ENVIO/RECEB │ TIPO │ LEN(PACOTE) │ N_PACOTE (head["h4"]) │ QTD_PACOTES (head["h3"]) │ CRC (caso seja envio)'.
    '''
    line = date + ' ' + time

    if tx == True:
        params = ['envio', str(type), str(pck_len), str(n_pck), str(pck_total), str(crc)]
    else:
        params = ['receb', str(type), str(pck_len)]
    for param in params:
        line += sep + param
        
    return line + '\n'

def file_write(path, content, mode):
    with open(path, mode, encoding='utf-8') as file:
        file.write(content)

class Message:
    def __init__(self) -> None:
        pass

    def head_pack(self, type: int, qt_pack: int, n_pack: int, pack_len: int, last_pack: int, cont: int):
        msg_head = to_bytes(type)
        if type == 1:
            msg_head += to_bytes(SERVER_ID) + BYTE1_FREE + to_bytes(qt_pack) + to_bytes(n_pack) + to_bytes(pack_len) + BYTE1_FREE*4
        elif type == 2: # confirmação -> handshake (olhar enunciado)
            msg_head += BYTE2_FREE + to_bytes(qt_pack) + to_bytes(n_pack) + to_bytes(pack_len) + to_bytes(last_pack) + BYTE2_FREE
        elif type == 3:
            msg_head += BYTE2_FREE + to_bytes(qt_pack) + to_bytes(cont) + to_bytes(pack_len) + BYTE1_FREE + to_bytes(cont - 1) + BYTE2_FREE
        elif type == 4: # confirmação -> handshake (olhar enunciado)
            msg_head += BYTE2_FREE + to_bytes(qt_pack) + to_bytes(n_pack) + to_bytes(pack_len) + BYTE1_FREE + to_bytes(cont - 1) + BYTE2_FREE
        elif type == 5:
            msg_head += BYTE2_FREE + to_bytes(qt_pack) + to_bytes(n_pack) + to_bytes(pack_len) + BYTE1_FREE + to_bytes(cont - 1) + BYTE2_FREE
        else:
            msg_head += BYTE2_FREE + to_bytes(qt_pack) + to_bytes(n_pack) + to_bytes(pack_len) + to_bytes(last_pack) + to_bytes(cont - 1) + BYTE2_FREE
        return msg_head

    def head_unpack(self, rx_head: bytearray):
        try:
            head = {'h0': rx_head[0], 'h1': rx_head[1],
                    'h2': rx_head[2], 'h3': rx_head[3],
                    'h4': rx_head[4], 'h5': rx_head[5],
                    'h6': rx_head[6], 'h7': rx_head[7],
                    'h8': rx_head[8], 'h9': rx_head[9]}
            return head
        
        except (TypeError, IndexError) as error:
            print(error)

    def build(self, head: bytearray, payload: bytearray, eop: bytearray = EOP):
        '''
        Recebe o HEAD, o PAYLOAD e o EOP (padrão igual a AA BB CC DD) e devolve a mensagem pronta.
    
        - Inputs
          - head: bytearray
          - payload: bytearray
          - O EOP já está definido como variável global e pode ser chamado pelo nome 'EOP'.
        '''
        try:
            return head + payload + eop
        except TypeError as error:
            print(error)

    def crc_build(self, payload):
        seq_str = payload.hex()

        s = unhexlify(seq_str)

        crc16 = crcmod.predefined.Crc('xmodem')
        crc16.update(s)

        crc = crc16.hexdigest()
        return crc
