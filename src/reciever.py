EXAMPLE_DATA = b'TTP0\x0chelaspafspaft-'

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

def parser(data, show_debug): #seperates data
    listed_data = list(data)
    get_prtv = listed_data[0:4]
    get_msglen = listed_data[len(get_prtv)]
    get_utf8msg = listed_data[len(get_prtv) + 1:len(get_prtv) + 1 + get_msglen]
    get_crc = listed_data[len(listed_data) - 2: len(listed_data)]

    #debug prints
    if show_debug == True:
        print("length of frame ", len(listed_data), "\n")
        print("protocol version ", get_prtv)
        print("msg length ", get_msglen)
        print("msg ", get_utf8msg)
        print("crc ", get_crc, "\n")
        print("full parsed packet ", listed_data)
    
    return get_prtv, get_msglen, get_utf8msg, get_crc, listed_data

def check_crc(recieved_frame, recieved_crc, show_debug): #check crc if packet is good
    CRC_computed = CRC16()
    CRC_computed.update(recieved_frame)
    value = CRC_computed.digest()

    CRC_high = (value >> 8) & 0xFF
    CRC_low  = value & 0xFF

    #compare
    listed_crc = [CRC_high] + [CRC_low]
    if listed_crc == recieved_crc:
        print("PACKET GOOD")
        packet_status = True
    else:
        print("PACKET BAD... DROPPING.")
        packet_status = False

    #debug prints
    if show_debug == True:
        print(hex(value))
        print(hex(CRC_high))
        print(hex(CRC_low), "\n")
        print(recieved_crc)

    return packet_status, CRC_high, CRC_low



PRTV, MSGLEN, UTF8MSG, CRC, FRAME = parser(EXAMPLE_DATA, True)
packet_status, CRC_high, CRC_low = check_crc(PRTV + [MSGLEN] + UTF8MSG, CRC, False)

print(packet_status)
# print("Full Frame", PRTV, MSGLEN, UTF8MSG, CRC, "\n")


