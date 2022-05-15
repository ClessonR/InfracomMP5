import socket
from threading import Thread


FORMAT = 'utf-8'
IP = "0.0.0.0"
PORT = 10000
ADDR = (IP, PORT)
BUFFER = 1024

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
#UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
UDPClientSocket.bind(ADDR)


def sender(server_address):
    while True:
        msg = input()
        UDPClientSocket.sendto(msg.encode(FORMAT), server_address)

def receiver():
    while True:
        msgFromServer = UDPClientSocket.recvfrom(1024)
        print(msgFromServer[0].decode(FORMAT), msgFromServer[1])
   
    

if __name__ == '__main__':
    server_ip = '179.152.187.178'
    server_port = 10000
    server_address = (server_ip, server_port)
    send = Thread(target=sender, args=[server_address])
    receive = Thread(target=receiver)
    send.start()
    receive.start()