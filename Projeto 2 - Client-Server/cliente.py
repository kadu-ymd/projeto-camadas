import random

COMANDOS = [b"\x00\x00\x00\x00", b"\x00\x00\xBB\x00", b"\xBB\x00\x00", b"\x00\xBB\x00", b"\x00\x00\xBB", b"\x00\xAA", b"\xBB\x00", b"\x00", b"\xBB"]

def sorteia_numero():
    '''Sorteia n entre 10 e 30'''
    return random.randint(10,30)

def encontra_comando():
    return COMANDOS[random.randint(0,8)]

def to_bytearray(n):
    comandos_escolhidos = []
    for i in range(n):
        comandos_escolhidos.append(b'\xff' + encontra_comando())

    comandos_escolhidos.append(b'\xff'*2)

    array = b''

    for cmd in comandos_escolhidos:
        array += cmd

    return array