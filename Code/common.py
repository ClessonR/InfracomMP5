import random
import socket
import select

FORMAT = 'utf-8'
BUFFER_RCV = 4096
BUFFER_SEND = 1024
SAMPLE_SIZE = 52428800

flag = True

def reset_flag():
    global flag
    flag = True


def udp_sender(UDPSocket: socket.socket, TCPSocket: socket.socket, server_addr):
    data = random.randbytes(SAMPLE_SIZE)
    data = [data[i:i+BUFFER_SEND] for i in range(0, len(data), BUFFER_SEND)]
    print(len(data))
    for count, package in enumerate(data):
        count = count.to_bytes(4, byteorder='little')
        package = count + package
        UDPSocket.sendto(package, server_addr)
    TCPSocket.sendall(len(data).to_bytes(4, byteorder='little'))    
    print("Done sending")
    

def tcp_receiver(TCPSocket: socket.socket):
    msg = TCPSocket.recv(4)
    
    global flag
    flag = False
    
    return int.from_bytes(msg, byteorder='little')
    
    
def isReadReady(sock, timeout=None):
        read_ready, _, _ = select.select([sock], [], [], timeout)
        return len(read_ready) > 0


def udp_receiver(UDPSocket: socket.socket):
    received_packages = []
    
    while flag:
        if isReadReady(UDPSocket, timeout=1):
            msg = UDPSocket.recvfrom(BUFFER_RCV)
            counter = msg[:4]
            received_packages.append(counter)
                
    
    print(f"Amount of packages received: {len(received_packages)}")