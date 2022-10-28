from client import Client
from server import Server
from threading import *

def main():
    server = Server()
    server_address = server.send_server_address()

    client0_thread = Thread(target=client0, args=(server_address,))
    client1_thread = Thread(target=client1, args=(server_address,))

    client0_thread.start()
    client1_thread.start()

def client0(server_address):
    client0 = Client(server_address)

def client1(server_address):
    client1 = Client(server_address)

main()
