from socket import *

class Server:
    def __init__(self):
        self.PORT = 4914
        self.IP = "localhost"
        self.BUFFER = 4096
        
        # Creating server socket
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((self.IP, self.PORT))
        self.socket.listen(2)

        self.clients_info = []
        self.clients_connections = []

