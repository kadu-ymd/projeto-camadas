from enlace import *

serialName = "COM5"  

com1 = enlace(serialName)

com1.enable()
print("esperando 1 byte de sacrifício")
rxBuffer, nRx = com1.getData(1)
com1.rx.clearBuffer()
time.sleep(.1)