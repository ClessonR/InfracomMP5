import random
import socket
import select
import time
import threading
import logging


FORMAT = "utf-8"
BUFFER_RCV = 4096
BUFFER_SEND = 1024
SAMPLE_SIZE = 52428800


def sender(UDPSocket: socket.socket, TCPSocket: socket.socket, server_addr):
    data = random.randbytes(SAMPLE_SIZE)
    logging.info(f"A random sample of {SAMPLE_SIZE} bytes has been generated.")
    data = [data[i : i + BUFFER_SEND] for i in range(0, len(data), BUFFER_SEND)]
    logging.info(f"The data has been split into {len(data)} packages. Each with a maximum size of {BUFFER_SEND} bytes.")
    logging.info(f"Initiating UDP transmission to {server_addr[0]}:{server_addr[1]}...")
    initial_time = time.perf_counter()
    total_size = 0
    for count, package in enumerate(data):
        count_bytes = count.to_bytes(4, byteorder="little")
        package = count_bytes + package
        total_size += len(package)
        logging.debug(f"Sending package {count}/{len(data)}...")
        logging.debug(f"Package size: {len(package)} bytes.")
        logging.debug(f"Package content: {package}")
        UDPSocket.sendto(package, server_addr)
    elapsed_time = time.perf_counter() - initial_time
    logging.info("UDP transmission has been completed.")
    print(f"Upload time: {elapsed_time} seconds.")
    print(f"Upload speed: {(total_size / elapsed_time)} bytes/second.")
    tcp_content = len(data).to_bytes(4, byteorder="little")
    TCPSocket.sendall(tcp_content)
    logging.info("The TCP message has been sent.")
    logging.debug(f"TCP message contents: {tcp_content}")


def stop_receiver(TCPSocket: socket.socket, stopReceived: threading.Event, dto: list):
    msg = TCPSocket.recv(4)
    packages_sent_count = int.from_bytes(msg, byteorder="little")
    dto.append(packages_sent_count)

    logging.info(f"The amount of packages that should have been received is {packages_sent_count}")

    stopReceived.set()

    logging.info("The flag responsible for stopping the receiver has been raised.")


def isReadReady(sock, timeout=None):
    read_ready, _, _ = select.select([sock], [], [], timeout)
    return len(read_ready) > 0


def receiver(UDPSocket: socket.socket, TCPSocket: socket.socket):
    received_packages = []
    stopReceived = threading.Event()

    dto = []  # Data Transfer Object

    stop_receiver_thread = threading.Thread(
        target=stop_receiver, args=[TCPSocket, stopReceived, dto]
    )
    stop_receiver_thread.start()

    logging.info("Initializing UDP reception...")
    initial_time = time.perf_counter()
    total_size = 0
    while not stopReceived.is_set():
        if isReadReady(UDPSocket, timeout=1):
            package = UDPSocket.recvfrom(BUFFER_RCV)[0]
            total_size += len(package)
            counter = package[:4]
            msg = package[4:]
            logging.debug(f"Received package {int.from_bytes(counter, byteorder='little')}...")
            logging.debug(f"Package size: {len(package)} bytes.")
            logging.debug(f"Package content: {msg}")
            received_packages.append(counter)
    elapsed_time = time.perf_counter() - initial_time
    logging.info("The flag responsible for stopping the receiver has been detected.")


    stop_receiver_thread.join()
    packages_sent_count = dto[0]

    print(f"Amount of packages received: {len(received_packages)}")
    print(
        f"Rate of loss: {((packages_sent_count - len(received_packages)) / packages_sent_count) * 100:.2f}%"
    )
    print(f"Download time: {elapsed_time} seconds.")
    print(f"Download speed: {(total_size / elapsed_time)} bytes/second.")

