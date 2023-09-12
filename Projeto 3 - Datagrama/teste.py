import math
imageR = 'Projeto 3 - Datagrama/img/imagem_enviada.png'
txBuffer = open(imageR, 'rb').read()
print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))

n_pck = math.ceil(len(txBuffer)/50)

var = 0

n_rest = n_pck

for i in range(1, n_pck):
    payload = txBuffer[var:50*i]

    pck_index = i.to_bytes(1, byteorder='little')
    pck_size = len(payload).to_bytes(1, byteorder='little')
    qt_pck = n_pck.to_bytes(1, byteorder='little')

    head = pck_index + pck_size + qt_pck
    print(head[0], head[1], head[2])
    # print(payload, len(payload), 50*i)
    var += 50
# print(txBuffer[var:], len(txBuffer[var:]), len(txBuffer)-var)



