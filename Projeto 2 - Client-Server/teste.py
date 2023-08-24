from cliente import *

n = sorteia_numero()
comandos_escolhidos = []
for i in range(n):
    comandos_escolhidos.append(b'\xff' + encontra_comando())

comandos_escolhidos.append(b'\xff'*2)

txBuffer = b''

for cmd in comandos_escolhidos:
    txBuffer += cmd

print(txBuffer)