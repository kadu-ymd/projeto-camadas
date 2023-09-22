from datetime import datetime 

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

def build_log(tx: bool, type: int, pck_total: int, pck_len: int, n_pck: int, crc: str = 'FFFF', date: str = get_date(), time: str = get_time(), sep: str = ' / ') -> str: 
    '''
    Constói o log no formato 'DATA HORA / ENVIO/RECEB / TIPO / LEN(PACOTE) / N_PACOTE (head["h4"]) / QTD_PACOTES (head["h3"]) /CRC (caso seja envio)'.
    '''
    line = date + ' ' + time

    if tx == True:
        params = ['envio', str(type), str(pck_len), str(n_pck), str(pck_total), str(crc)]
    else:
        params = ['receb', str(type), str(pck_len)]

    for param in params:
        line += sep + param


    return line + '\n'

def log_write(path: str, log: str, mode: str) -> None:
    with open(path, mode) as file:
        file.write(log)

log = build_log(tx=True, type=3, pck_total=14, pck_len=128, n_pck=1)

log2 = build_log(tx=True, type=3, pck_total=14, pck_len=128, n_pck=2)

with open('Projeto 4 - PPP/logs/Server1.txt', 'w') as file:
    file.write(log)

with open('Projeto 4 - PPP/logs/Server1.txt', 'a') as file:
    file.write(log2)

