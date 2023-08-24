from cliente import *

comandos = ["\x00\x00\x00\x00", "\x00\x00\xBB\x00", "\xBB\x00\x00", "\x00\xBB\x00", "\x00\x00\xBB", "\x00\xAA", "\xBB\x00", "\x00", "\xBB"]

n = sorteia_numero()
comandos_escolhidos = []
for i in range(n):
    comandos_escolhidos.append(encontra_comando(comandos))
            
print(comandos_escolhidos)