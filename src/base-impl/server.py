import socket
import reciever as rx
import errcheck as errchk

HOST = "127.0.0.1"  # Localhost
PORT = 65432        # Non-privileged port (> 1023)
ACK = b'\x01'
NACK = b'\x02'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            buffer = b""
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                buffer += data

                while len(buffer) >= 4:
                    frame_len = int.from_bytes(buffer[:4], byteorder="big")
                    if len(buffer) < 4 + frame_len:
                        break
                    frame = buffer[4:4 + frame_len]
                    buffer = buffer[4 + frame_len:]

                    PRTVrx, MSGLENrx, TYPErx, UTF8MSGrx, CRCrx, FRAMErx = rx.parser(frame, True)
                    packet_status, CRC_high, CRC_low = rx.check_crc(PRTVrx + [MSGLENrx] + [TYPErx] + UTF8MSGrx, CRCrx, True)

                    print(packet_status, "\n")
                    if packet_status:
                        conn.sendall(ACK)
                    else:
                        conn.sendall(NACK)
