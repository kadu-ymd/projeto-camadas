import crcmod.predefined
from binascii import unhexlify
from utils import *

seq = b'\xd9\x1f\xd0\x04\xb2\xb4\xd9\x1f\xd0\x04\xb2\xb4\xd9\x1f\xd0\x04\xb2\xb4\xd9\x1f\xd0\x04\xb2\xb4\xd9\x1f\xd0\x04\xb2\xb4\xd9\x1f\xd0\x04\xb2\xb4\xd9\x1f\xd0\x04\xb2\xb4\xd9\x1f\xd0\x04\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0\x8f\xbf\x01\x0e\xea\xd0\xa6q1\xe3\xe1\x00\x00\x00\x00IEND\xaeB`\x82'

seq_str = seq.hex()

s = unhexlify(seq_str)

crc16 = crcmod.predefined.Crc('xmodem')
crc16.update(s)

crc = crc16.hexdigest()

head = b'\xff'*8 + bytes.fromhex(crc)

print(hex(head[8]), hex(head[9]))