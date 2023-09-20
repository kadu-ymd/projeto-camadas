EOP = b'\xAA\xBB\xCC\xDD'
SERVER_ID = 1

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
    