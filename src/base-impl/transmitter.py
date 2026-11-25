# All """placeholder""" is AI generated but the code base is not


class CRC16:
    """CRC-16/IBM implementation with lookup table."""

    def __init__(self, polynomial=0xA001, init=0xFFFF, xor_out=0x0000):
        """Initialize CRC with polynomial, initial value, and output XOR."""
        self.polynomial = polynomial
        self.init = init
        self.xor_out = xor_out

        self.mask = 0xFFFF
        self.table = self._make_table()
        self.reset()

    def reset(self):
        """Reset CRC to initial value."""
        self.crc = self.init

    def _make_table(self):
        """Generate 256-entry lookup table for fast CRC calculation."""
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
        """Update CRC with new data bytes."""
        for b in data:
            self.crc = self.table[(self.crc ^ b) & 0xFF] ^ (self.crc >> 8)
            self.crc &= self.mask

    def digest(self):
        """Return final CRC value as integer."""
        return self.crc ^ self.xor_out

    def hexdigest(self):
        """Return final CRC value as 4-digit hex string."""
        return f"{self.digest():04X}"

def framebuildernocrc(PRTV, MSGLint, TYPE, MSG):
    """Build TTP0 frame without CRC (for CRC calculation)."""
    MSGLbytes = MSGLint.to_bytes(1, byteorder="big")
    TYPEbytes = TYPE.to_bytes(1, byteorder="big")
    frame = PRTV + MSGLbytes + TYPEbytes + MSG
    print(frame)
    return frame

def framebuilder(PRTV, MSGLint, TYPE, MSG, CRCint_high, CRCint_low):
    """Build complete TTP0 frame with CRC bytes appended."""
    MSGLbytes = MSGLint.to_bytes(1, byteorder="big")
    TYPEbytes = TYPE.to_bytes(1, byteorder="big")
    CRCbytes_high = CRCint_high.to_bytes(1, byteorder="big")
    CRCbytes_low = CRCint_low.to_bytes(1, byteorder="big")
    frame = PRTV + MSGLbytes + TYPEbytes + MSG + CRCbytes_high + CRCbytes_low
    print(frame)
    return frame

def fulltcpframebuilder(listed_data, debug_mode):
    frameLenBytes = 4 + len(listed_data)
    full_frame = frameLenBytes + listed_data
    if debug_mode == True:
        print(frameLenBytes, full_frame)

    return full_frame



