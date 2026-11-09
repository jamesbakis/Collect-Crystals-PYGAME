import os
import socket
from dotenv import load_dotenv

def startServer():
    load_dotenv()

    HOST = "0.0.0.0"
    PORT = 5000

    buffer = 1024

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind((HOST, PORT))

    print(f"Server is running on {HOST}:{PORT}")

    while True:
        data, addr = serverSocket.recvfrom(buffer)
        print(f"Received from {addr}: {data.decode()}")

if __name__ == "__main__":
    startServer()