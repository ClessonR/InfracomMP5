import random
import socket
import select
import time

FORMAT = 'utf-8'
BUFFER_RCV = 4096
BUFFER_SEND = 1024
SAMPLE_SIZE = 52428800

flag = True


def udp_sender(UDPSocket: socket.socket, TCPSocket: socket.socket, server_addr):
    data = random.randbytes(SAMPLE_SIZE)
    print(f"Random sample data of size {len(data)} bytes has been created.")
    data = [data[i:i+BUFFER_SEND] for i in range(0, len(data), BUFFER_SEND)]
    print(f"Data has been split into {len(data)} packages.")
    print("Initiating UDP transmission...")
    initial_time = time.perf_counter()
    total_size = 0
    for count, package in enumerate(data):
        count = count.to_bytes(4, byteorder='little')
        package = count + package
        total_size += len(package)
        UDPSocket.sendto(package, server_addr)
    elapsed_time = time.perf_counter() - initial_time
    print(f"UDP transmission has been completed.")
    print(f"Upload time: {elapsed_time} seconds.")
    print(f"Upload speed: {(total_size / elapsed_time)} bytes/second.")
    TCPSocket.sendall(len(data).to_bytes(4, byteorder='little'))    
    print("TCP transmission has been completed.")
    

def tcp_receiver(TCPSocket: socket.socket):
    msg = TCPSocket.recv(4)
    packages_sent = int.from_bytes(msg, byteorder='little')
    
    print(f"Amount of packages sent: {packages_sent}")
    
    global flag
    flag = False
    
    print("The flag responsible for stopping the UDP Receiver has been raised.")

    
    
def isReadReady(sock, timeout=None):
        read_ready, _, _ = select.select([sock], [], [], timeout)
        return len(read_ready) > 0


def udp_receiver(UDPSocket: socket.socket):
    received_packages = []
    
    print("Initiating UDP reception...")
    while flag:
        if isReadReady(UDPSocket, timeout=1):
            msg = UDPSocket.recvfrom(BUFFER_RCV)
            counter = msg[:4]
            received_packages.append(counter)
    print("The flag has been detected. UDP reception has been completed.")
                    
    print(f"Amount of packages received: {len(received_packages)}")