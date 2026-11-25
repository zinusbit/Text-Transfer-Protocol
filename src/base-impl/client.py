import transmitter as tx
import reciever as rx
import socket as socket
import errcheck as errchk

# parameters for tx
HOST = "127.0.0.1"
PORT = 65432


#send data
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
      PROTOCOL_VERSION = bytes([0x54, 0x54, 0x50, 0x30]) #TTP0 (texttransfer protocol v0)
      message = input()
      utf8msg = message.encode("utf-8")
      msglen = len(utf8msg)
      type = 0x04
      #tx
      crc = tx.CRC16()
      crc.update(tx.framebuildernocrc(PROTOCOL_VERSION, msglen, type, utf8msg))
      value = crc.digest()

      CRC_high = (value >> 8) & 0xFF
      CRC_low  = value & 0xFF

      #all debug info
      # print(type(PROTOCOL_VERSION)) 
      # print(type(msglen))
      # print(type(utf8msg))
      # print(type(crc))

      print("you can only put 31 bytes in the buffer\n")

      #check the bytes in the buffer
      ChkBuff = errchk.checkbuffer(msglen) 
      ChkBuff.checkmaxchars()
      ChkBuff.checknochars()
      
      DATArx = tx.framebuilder(PROTOCOL_VERSION, msglen, type, utf8msg, CRC_high, CRC_low)

      length_prefix = len(DATArx).to_bytes(4, byteorder="big")
      s.sendall(length_prefix + DATArx)

      data = s.recv(1)
      if data == b'\x01':
           print("data sucessfully sent")
      elif data == b'\x02':
           print("data frame bad... closing.")
           # resendframe()
