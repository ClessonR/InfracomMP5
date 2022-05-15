import socket
import random
from threading import Thread
import time

SAMPLE_SIZE = 52428800
FORMAT = 'utf-8'
IP = '192.168.15.131'
PORT = 10000
ADDR = (IP, PORT)

UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
UDPSocket.bind(ADDR)
print('Server is running')

#print("O servidor UDP está pronto")
#
#data = random.randbytes(SAMPLE_SIZE)

def receiver():
    #isDone = False
    #while not isDone:
    #    msg = UDPSocket.recv()
    while True:
        msg = UDPSocket.recvfrom(1024)
        print(msg[0].decode(FORMAT), msg[1])


def sender(client_addr):
    while True:
        msg = input()
        UDPSocket.sendto(msg.encode(FORMAT), client_addr)


if __name__ == "__main__":
    client_ip = '179.152.187.178'
    client_port = 10000
    client_addr = (client_ip, client_port)
    send = Thread(target=sender, args=[client_addr])
    receive = Thread(target=receiver)
    send.start()
    receive.start()
