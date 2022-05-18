import random
import socket
import select
import time
import threading


FORMAT = "utf-8"
BUFFER_RCV = 4096
BUFFER_SEND = 1024
SAMPLE_SIZE = 52428800


def sender(UDPSocket: socket.socket, TCPSocket: socket.socket, server_addr):
    data = random.randbytes(SAMPLE_SIZE)
    print(f"Random sample data of size {len(data)} bytes has been created.")
    data = [data[i : i + BUFFER_SEND] for i in range(0, len(data), BUFFER_SEND)]
    print(f"Data has been split into {len(data)} packages.")
    print("Initiating UDP transmission...")
    initial_time = time.perf_counter()
    total_size = 0
    for count, package in enumerate(data):
        count = count.to_bytes(4, byteorder="little")
        package = count + package
        total_size += len(package)
        UDPSocket.sendto(package, server_addr)
    elapsed_time = time.perf_counter() - initial_time
    print(f"UDP transmission has been completed.")
    print(f"Upload time: {elapsed_time} seconds.")
    print(f"Upload speed: {(total_size / elapsed_time)} bytes/second.")
    TCPSocket.sendall(len(data).to_bytes(4, byteorder="little"))
    print("TCP transmission has been completed.")


def stop_receiver(TCPSocket: socket.socket, stopReceived: threading.Event, dto: list):
    msg = TCPSocket.recv(4)
    packages_sent_count = int.from_bytes(msg, byteorder="little")
    dto.append(packages_sent_count)

    print(f"Amount of packages that should have been received: {packages_sent_count}")

    stopReceived.set()

    print("The flag responsible for stopping the UDP Receiver has been raised.")


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

    print("Initiating UDP reception...")
    initial_time = time.perf_counter()
    total_size = 0
    while not stopReceived.is_set():
        if isReadReady(UDPSocket, timeout=1):
            msg = UDPSocket.recvfrom(BUFFER_RCV)
            total_size += len(msg)
            counter = msg[:4]
            received_packages.append(counter)
    elapsed_time = time.perf_counter() - initial_time
    print("The flag has been detected. UDP reception has been completed.")

    packages_sent_count = dto[0]

    print(f"Amount of packages received: {len(received_packages)}")
    print(
        f"Rate of loss: {((packages_sent_count - len(received_packages)) / packages_sent_count) * 100:.2f}%"
    )
    print(f"Download time: {elapsed_time} seconds.")
    print(f"Download speed: {(total_size / elapsed_time)} bytes/second.")

    stop_receiver_thread.join()
