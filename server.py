from socket import *
from threading import *


class Server:
    def __init__(self):
        self.PORT = 4914
        self.IP = "localhost"
        self.BUFFER = 4096
        # String aleatória para usar o split
        self.SEPARATOR = "αβήταGreΕεekalphaΣσςbet.svg"

        # Creating server socket
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((self.IP, 0))
        self.socket.listen(2)

        self.clients_info = []
        self.clients_connections = []

        search_connections_thread = Thread(
            target=self.search_connections, args=())
        search_connections_thread.start()

    # Simplesmente retorna o endereço do server
    def send_server_address(self):
        return (self.IP, self.socket.getsockname()[1])

    # Espera por duas conexões e troca os endereços dos clientes
    def search_connections(self):
        for i in range(2):
            connection_socket, address = self.socket.accept()

            self.clients_connections.append(connection_socket)

            # Nome, endereço
            info = f"{i}{self.SEPARATOR}{connection_socket.recv(self.BUFFER).decode()}"

            self.clients_info.append(info)

        self.clients_connections[0].send(self.clients_info[1].encode())
        # Espera uma mensagem de confirmação
        self.clients_connections[0].recv(self.BUFFER)
        self.clients_connections[1].send(self.clients_info[0].encode())
        print("Enviado!")

        self.clients_connections[0].close()
        self.clients_connections[1].close()

        self.clients_info = []
        self.clients_connections = []
        self.socket.close()
