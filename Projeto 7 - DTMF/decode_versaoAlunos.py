from suaBibSignal import *
import peakutils 
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time

FREQUENCIAS = {
        0: [941, 1336],
        1: [697, 1209],
        2: [697, 1336],
        3: [697, 1477],
        4: [770, 1209],
        5: [770, 1336],
        6: [770, 1477],
        7: [852, 1209],
        8: [852, 1336],
        9: [852, 1477],
    }

def encontraTecla(picos):
    def encontraFrequencia(diff=600):
        for pico in picos:
            for _, value in FREQUENCIAS.items():
                if abs(pico - value[i]) < diff:
                    diff, frequencia = abs(pico-value[0]), value[i]
        return frequencia

    def filter_function(item):
        valor_desejado = frequencia
        _, value = item
        if value[i] == valor_desejado:
            return True
        return False
    
    i = 0
    frequencia = encontraFrequencia()
    frequencia_filtrada = dict(filter(filter_function, FREQUENCIAS.items()))

    i = 1
    frequencia = encontraFrequencia()
    frequencia_filtrada1 = dict(filter(filter_function, frequencia_filtrada.items()))

    for key in frequencia_filtrada1:
        return key

def todB(s):
    # Transforma intensidade acustica em dB
    sdB = 10 * np.log10(s)
    return sdB


def main():
    signal = signalMeu()
    f_amostragem = 44100
    sd.default.samplerate = f_amostragem  # taxa de amostragem
    sd.default.channels = 2  # numCanais -> o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    duration = (2)  

    # calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes) durante a gracação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação

    num_amostras = f_amostragem * duration

    # faca um print na tela dizendo que a captacao comecará em n segundos. e entao
    # use um time.sleep para a espera

    for n in range(3, 0, -1):
        print(f"A captação do sinal começará em {n} segundos...", end="\r")
        time.sleep(1)

    # Ao seguir, faca um print informando que a gravacao foi inicializada
    # print(' ', end='\r')
    print("A gravação foi iniciada!                     ", end="\r")

    # para gravar, utilize
    audio = sd.rec(int(num_amostras), f_amostragem)
    sd.wait()
    print("...Fim da gravação!                    ")

    # analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    # extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações).

    dados = [audio[i][1] for i in range(len(audio))]

    # # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!

    tempo = np.linspace(0, duration, num_amostras)

    # # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) .

    plt.figure()
    plt.plot(tempo, dados)
    plt.grid(True)
    plt.title('Áudio (Hz) x Tempo (s)')
    

    ## Calcule e plote o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias

    xf, yf = signal.calcFFT(dados, f_amostragem)

    signal.plotFFT(dados, f_amostragem)

    # #agora, voce tem os picos da transformada, que te informam quais sao as frequencias mais presentes no sinal. Alguns dos picos devem ser correspondentes às frequencias do DTMF!
    # #Para descobrir a tecla pressionada, voce deve extrair os picos e compara-los à tabela DTMF
    # #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    # # para extrair os picos, voce deve utilizar a funcao peakutils.indexes(,,)
    # # Essa funcao possui como argumentos dois parâmetros importantes: "thres" e "min_dist".
    # # "thres" determina a sensibilidade da funcao, ou seja, quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    # #"min_dist" é relatico tolerancia. Ele determina quao próximos 2 picos identificados podem estar, ou seja, se a funcao indentificar um pico na posicao 200, por exemplo, só identificara outro a partir do 200+min_dis. Isso evita que varios picos sejam identificados em torno do 200, uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.
    # # Comece com os valores:

    index = peakutils.indexes(yf, thres=0.15, min_dist=50)

    # #printe os picos encontrados!
    # # Aqui você deverá tomar o seguinte cuidado: A funcao  peakutils.indexes retorna as POSICOES dos picos. Não os valores das frequências onde ocorrem! Pense a respeito

    picos = [xf[i] for i in index]

    print(picos)

    tecla = encontraTecla(picos)

    print(f'A tecla detectada foi {tecla}!')

    # #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    # #print o valor tecla!!!
    # #Se acertou, parabens! Voce construiu um sistema DTMF

    # #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla.

    # ## Exiba gráficos do fourier do som gravados
    plt.show()

if __name__ == "__main__":
    main()
