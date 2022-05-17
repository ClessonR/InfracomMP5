import socket

from common import sender, receiver


FORMAT = "utf-8"
IP = "0.0.0.0"
UDP_PORT = 10002
TCP_PORT = 10003
UDP_ADDR = (IP, UDP_PORT)
TCP_ADDR = (IP, TCP_PORT)


UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPSocket.bind(UDP_ADDR)

TCPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)


if __name__ == "__main__":
    server_ip = "localhost"
    server_udp_port = 10000
    server_tcp_port = 10001
    server_udp_addr = (server_ip, server_udp_port)
    server_tcp_addr = (server_ip, server_tcp_port)

    TCPSocket.connect(server_tcp_addr)

    sender(UDPSocket, TCPSocket, server_udp_addr)
    receiver(UDPSocket, TCPSocket)

    TCPSocket.close()
