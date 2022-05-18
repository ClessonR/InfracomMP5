import socket
import logging

from time import sleep

from common import sender, receiver


FORMAT = "utf-8"
ALLOWED_CONN_ATTEMPTS = 5
IP = "0.0.0.0"
PORT = 10001
ADDR = (IP, PORT)

LOG_LEVEL = logging.INFO

logging.basicConfig(level=LOG_LEVEL)


UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPSocket.bind(ADDR)
logging.info(f"UDP Socket binded to {IP}:{PORT}")

TCPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)


if __name__ == "__main__":
    server_ip = input("Enter the IP of the server: ")
    server_port = int(input("Enter the port of the server: "))
    server_addr = (server_ip, server_port)

    allowed_attempts_left = ALLOWED_CONN_ATTEMPTS
    while allowed_attempts_left > 0:
        try:
            logging.info(f"Attempting to connect to the server at {server_ip}:{server_port}")
            TCPSocket.connect(server_addr)
            logging.info(f"TCP Connection to the server at {server_ip}:{server_port} has been established.")
            break
        except ConnectionRefusedError:
            allowed_attempts_left -= 1
            logging.error(f"Failed to establish TCP connection to the server at {server_ip}:{server_port}. Trying again in 5 seconds. ({allowed_attempts_left} attempts left)")
            sleep(5)
    else:
        logging.critical(f"Failed to establish TCP connection to the server at {server_ip}:{server_port} after {ALLOWED_CONN_ATTEMPTS} attempts. Exiting.")
        raise ConnectionRefusedError
            

    sender(UDPSocket, TCPSocket, server_addr)
    receiver(UDPSocket, TCPSocket)

    TCPSocket.close()
