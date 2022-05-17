import socket

from common import sender, receiver

FORMAT = "utf-8"
IP = "0.0.0.0"
UDP_PORT = 10000
TCP_PORT = 10001
UDP_ADDR = (IP, UDP_PORT)
TCP_ADDR = (IP, TCP_PORT)


UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPSocket.bind(UDP_ADDR)

TCPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPSocket.bind(TCP_ADDR)


if __name__ == "__main__":
    client_ip = "localhost"
    client_udp_port = 10002
    client_udp_addr = (client_ip, client_udp_port)

    TCPSocket.listen(1)
    conn, addr = TCPSocket.accept()

    receiver(UDPSocket, conn)
    sender(UDPSocket, conn, client_udp_addr)

    conn.close()
    TCPSocket.close()
