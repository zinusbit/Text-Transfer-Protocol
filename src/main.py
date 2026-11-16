PROTOCOL_VERSION = bytes([0x54, 0x54, 0x50, 0x30]) #TTP0 (texttransfer protocol v0)
MESSAGE = input()
UTF8MSG = MESSAGE.encode("utf-8")
MSGLEN = len(MESSAGE)
CRC = 12

class NoChars(Exception):
    pass
def checkbuffer(MSGLEN):
    if MSGLEN == 0:
        raise NoChars("No Chars in the buffer")
    return MESSAGE

def framebuilder(PRTV, MSGLint, MSG, CRCint):
    MSGLbytes = MSGLint.to_bytes(1, byteorder="big")
    CRCbytes = CRCint.to_bytes(1, byteorder="big")
    print(type(PRTV))
    print(type(MSGLint))
    print(type(MSGLbytes))
    print(type(MSG))
    print(type(CRC))
    print()
    frame = PRTV + MSGLbytes + MSG + CRCbytes #prot_version, msg length, msg, crc
    print(frame)
    return framebuilder

print(type(PROTOCOL_VERSION))
print(type(MSGLEN))
print(type(UTF8MSG))
print(type(CRC))
print("you can only put 31 characters in the buffer\n")
checkbuffer(MSGLEN)

framebuilder(PROTOCOL_VERSION, MSGLEN, UTF8MSG, CRC)


