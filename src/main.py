class CRC16: #taken from a old project.
    def __init__(self, polynomial=0xA001, init=0xFFFF, xor_out=0x0000):
        self.polynomial = polynomial
        self.init = init
        self.xor_out = xor_out

        self.mask = 0xFFFF
        self.table = self._make_table()
        self.reset()

    def reset(self):
        self.crc = self.init

    def _make_table(self):
        table = []
        for i in range(256):
            crc = i
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ self.polynomial
                else:
                    crc >>= 1
            table.append(crc & 0xFFFF)
        return table

    def update(self, data: bytes):
        for b in data:
            self.crc = self.table[(self.crc ^ b) & 0xFF] ^ (self.crc >> 8)
            self.crc &= self.mask

    def digest(self):
        return self.crc ^ self.xor_out

    def hexdigest(self):
        return f"{self.digest():04X}"

class NoChars(Exception):
    pass

def checkbuffer(MSGLEN):
    if MSGLEN == 0:
        raise NoChars("No Chars in the buffer")
    return MESSAGE

def framebuildernocrc(PRTV, MSGLint, MSG):
    MSGLbytes = MSGLint.to_bytes(1, byteorder="big")
    frame = PRTV + MSGLbytes + MSG #prot_version, msg length, msg
    print(frame)
    return frame

def framebuilder(PRTV, MSGLint, MSG, CRCint_high, CRCint_low):
    MSGLbytes = MSGLint.to_bytes(1, byteorder="big")
    CRCbytes_high = CRCint_high.to_bytes(1, byteorder="big")
    CRCbytes_low = CRCint_low.to_bytes(1, byteorder="big")
    frame = PRTV + MSGLbytes + MSG + CRCbytes_high + CRCbytes_low #prot_version, msg length, msg, crc
    print(frame)
    return framebuilder

PROTOCOL_VERSION = bytes([0x54, 0x54, 0x50, 0x30]) #TTP0 (texttransfer protocol v0)
MESSAGE = input()
UTF8MSG = MESSAGE.encode("utf-8")
MSGLEN = len(MESSAGE)

CRC = CRC16()
CRC.update(framebuildernocrc(PROTOCOL_VERSION, MSGLEN, UTF8MSG))
value = CRC.digest()

CRC_high = (value >> 8) & 0xFF
CRC_low  = value & 0xFF

print(type(PROTOCOL_VERSION))
print(type(MSGLEN))
print(type(UTF8MSG))
print(type(CRC))
print("you can only put 31 characters in the buffer\n")
checkbuffer(MSGLEN)

framebuilder(PROTOCOL_VERSION, MSGLEN, UTF8MSG, CRC_high, CRC_low)


