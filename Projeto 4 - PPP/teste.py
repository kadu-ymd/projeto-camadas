STD_HEAD = b'\xff'*12
STD_EOP = b'\xee'*3
payload = b'\xaa'
print(STD_HEAD+b'\xuu'+STD_EOP)