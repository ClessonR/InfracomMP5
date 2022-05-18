import socket
import logging

from common import sender, receiver

FORMAT = "utf-8"
IP = "0.0.0.0"
PORT = 10000
ADDR = (IP, PORT)

LOG_LEVEL = logging.INFO

logging.basicConfig(level=LOG_LEVEL)


UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPSocket.bind(ADDR)
logging.info(f"UDP Socket binded to {IP}:{PORT}")

TCPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPSocket.bind(ADDR)
logging.info(f"TCP Socket binded to {IP}:{PORT}")


if __name__ == "__main__":
    client_port = int(input("Enter the port of the client: "))
    logging.info("Waiting for connection...")
    TCPSocket.listen(1)
    conn, client_addr = TCPSocket.accept()
    logging.info(f"TCP Connection from {client_addr[0]}:{client_addr[1]} has been established.")

    client_ip = client_addr[0]
    client_addr = (client_ip, client_port)

    receiver(UDPSocket, conn)
    sender(UDPSocket, conn, client_addr)

    conn.close()
    TCPSocket.close()
