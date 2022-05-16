
import socket
import random
from threading import Thread, Lock

from common import tcp_receiver, udp_sender, udp_receiver

FORMAT = 'utf-8'
IP = "0.0.0.0"
UDP_PORT = 10000
TCP_PORT = 10001
UDP_ADDR = (IP, UDP_PORT)
TCP_ADDR = (IP, TCP_PORT)


UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPSocket.bind(UDP_ADDR)

TCPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPSocket.bind(TCP_ADDR)
   

if __name__ == '__main__':
    client_ip = "179.152.187.178"
    client_udp_port = 10002
    client_udp_addr = (client_ip, client_udp_port)
    
    TCPSocket.listen(1)
    conn, addr = TCPSocket.accept()
    
    udp_receiver_thread = Thread(target=udp_receiver, args=[UDPSocket])
    tcp_receiver_thread = Thread(target=tcp_receiver, args=[conn])
    
    udp_receiver_thread.start()
    tcp_receiver_thread.start()
    
    udp_receiver_thread.join()
    tcp_receiver_thread.join()
    
    udp_sender(UDPSocket, conn, client_udp_addr)
    
    conn.close()
    TCPSocket.close()
    