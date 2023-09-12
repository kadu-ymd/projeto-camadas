imageR = './img/imagem_enviada.png'
txBuffer = open(imageR, 'rb').read()
print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))

print(txBuffer)

