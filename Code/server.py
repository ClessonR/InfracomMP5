
import socket
import random
from threading import Thread, Lock


FORMAT = 'utf-8'
IP = "0.0.0.0"
UDP_PORT = 10000
TCP_PORT = 10001
ADDR = (IP, UDP_PORT)
BUFFER_RCV = 4096
BUFFER_SEND = 1024
SAMPLE_SIZE = 52428800


UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPSocket.bind(ADDR)

        

def udp_receiver():
    recvd_packeges = []
    try:
        while True:
            msg = UDPSocket.recvfrom(BUFFER_RCV)
            counter = msg[:4]
            recvd_packeges.append(counter)
                
    except KeyboardInterrupt:
        print(f"recvd_packeges: {len(recvd_packeges)}")


def udp_sender(server_addr):
    data = random.randbytes(SAMPLE_SIZE)
    data = [data[i:i+BUFFER_SEND] for i in range(0, len(data), BUFFER_SEND)]
    print(len(data))
    for count, package in enumerate(data):
        count = count.to_bytes(4, byteorder='little')
        package = count + package
        UDPSocket.sendto(package, server_addr)
    print("Done sending")
   

if __name__ == '__main__':
    client_ip = "179.152.187.178"
    client_udp_port = 10000
    client_udp_addr = (client_ip, client_udp_port)
    
    udp_receiver()
    udp_sender(client_udp_addr)