import transmitter as tx
import reciever as rx

# parameters for tx
PROTOCOL_VERSION = bytes([0x54, 0x54, 0x50, 0x30]) #TTP0 (texttransfer protocol v0)
MESSAGE = input()
UTF8MSG = MESSAGE.encode("utf-8")
MSGLEN = len(MESSAGE)
TYPE = 0x04


#tx
CRC = tx.CRC16()
CRC.update(tx.framebuildernocrc(PROTOCOL_VERSION, MSGLEN, TYPE, UTF8MSG))
value = CRC.digest()

CRC_high = (value >> 8) & 0xFF
CRC_low  = value & 0xFF

#all debug info
print(type(PROTOCOL_VERSION)) 
print(type(MSGLEN))
print(type(UTF8MSG))
print(type(CRC))

print("you can only put 31 bytes in the buffer\n")

#check the bytes in the buffer
ChkBuff = tx.checkbuffer(MSGLEN) 
ChkBuff.checkmaxchars()
ChkBuff.checknochars()

#build frame
DATArx = tx.framebuilder(PROTOCOL_VERSION, MSGLEN, TYPE, UTF8MSG, CRC_high, CRC_low)

#rx
PRTVrx, MSGLENrx, TYPErx, UTF8MSGrx, CRCrx, FRAMErx = rx.parser(DATArx, True)
packet_status, CRC_high, CRC_low = rx.check_crc(PRTVrx + [MSGLENrx] + [TYPErx] + UTF8MSGrx, CRCrx, True)

print(packet_status, "\n")
