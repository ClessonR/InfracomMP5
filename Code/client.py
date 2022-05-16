import socket
import random
from threading import Thread


FORMAT = 'utf-8'
IP = "0.0.0.0"
UDP_PORT = 10000
TCP_PORT = 10001
UDP_ADDR = (IP, UDP_PORT)
TCP_ADDR = (IP, TCP_PORT)
BUFFER_RCV = 4096
BUFFER_SEND = 1024
BUFFER_SIZE = 10240
SAMPLE_SIZE = 52428800
#BUFFER_SIZE = 10
#SAMPLE_SIZE = 101


UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPSocket.bind(UDP_ADDR)


def udp_sender(server_addr):
    data = random.randbytes(SAMPLE_SIZE)
    data = [data[i:i+BUFFER_SIZE] for i in range(0, len(data), BUFFER_SIZE)]
    print(len(data))
    for count, package in enumerate(data):
        count = count.to_bytes(4, byteorder='little')
        package = count + package
        UDPSocket.sendto(package, server_addr)
   
    
if __name__ == '__main__':
    server_ip = "179.186.140.143"
    server_udp_port = 10000
    server_udp_addr = (server_ip, server_udp_port)
    
    udp_sender(server_udp_addr)