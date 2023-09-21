from datetime import datetime 

EOP = b'\xAA\xBB\xCC\xDD'
SERVER_ID = 1
BYTE1_FREE = b'\xff'
BYTE2_FREE = b'\xff\xff'

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

def is_package_ok(rx_head: bytearray, rx_payload: bytearray, rx_eop: bytearray, cont: int):
    last_pckg = message_head(rx_head)['h7']
    if (cont - 1) == last_pckg:
        return True
    else:
        return False

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

class Message:
    # def __init__(self, type: int, qtd: int, n_pck: int, cont: int) -> None:
    #     self.qtd = to_bytes(qtd)
    #     self.type = type
    #     self.n = to_bytes(n_pck)
    #     self.cont = cont


    # def build_head(self) -> bytearray:
    #     try:
    #         if self.type == 1:
    #             return to_bytes(self.type) + to_bytes(SERVER_ID) + b'\xff' + self.qtd + self.n + b'\xff\xff' + to_bytes(self.cont - 1) + b'\xff\xff'

    #         elif self.type == 2:
    #             return to_bytes(self.type) + b'\xff\xff' + self.qtd + self.n + b'\xff\xff' + to_bytes(self.cont - 1) + b'\xff\xff'

    #         elif self.type == 3:
    #             return to_bytes(self.type) + b'\xff\xff' + self.qtd + self.n + b'\xff' + b'\xff' + to_bytes(self.cont - 1) + b'\xff\xff'
            
    #         elif self.type == 4:
    #             return to_bytes(self.type) + b'\xff\xff' + self.qtd + self.n + b'\xff\xff' + to_bytes(self.cont - 1) + b'\xff\xff'
            
    #         elif self.type == 5:
    #             return to_bytes(self.type) + b'\xff\xff' + self.qtd + self.n + b'\xff\xff' + to_bytes(self.cont - 1) + b'\xff\xff'
            
    #         else:
    #             pass
    #     except:
    #         pass

    #     pass

    def __init__(self) -> None:
        pass

    def build(self, head: bytearray, payload: bytearray, eop: bytearray = EOP) -> bytearray:
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

