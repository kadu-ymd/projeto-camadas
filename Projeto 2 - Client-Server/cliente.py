import random
def sorteia_numero():
    '''Sorteia n entre 10 e 30'''
    return random.randint(10,30)

def encontra_comando(comandos):
    return comandos[random.randint(0,8)]