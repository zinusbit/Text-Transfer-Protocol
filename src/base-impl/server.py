import socket
import reciever as rx
import errcheck as errchk

HOST = "127.0.0.1"  # Localhost
PORT = 65432        # Non-privileged port (> 1023)
ACK = b'\x01'
NACK = b'\x02'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            print(data, "\n")
            PRTVrx, MSGLENrx, TYPErx, UTF8MSGrx, CRCrx, FRAMErx = rx.parser(data, True)
            packet_status, CRC_high, CRC_low = rx.check_crc(PRTVrx + [MSGLENrx] + [TYPErx] + UTF8MSGrx, CRCrx, True)

            print(packet_status, "\n")
            #check the bytes in the buffer
            if packet_status == True:
                conn.sendall(ACK)
            if not data:
                print("badframe...")
                conn.sendall(NACK)