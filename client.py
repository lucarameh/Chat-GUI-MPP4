from distutils.file_util import write_file
from importlib.util import set_loader
import tkinter
import tkinter.scrolledtext
from tkinter import Button, Entry, simpledialog, filedialog
from datetime import datetime
from socket import *
from time import *
from threading import *
import shutil
import os

class Client:
    def __init__(self, server_address):
        self.BUFFER = 4096
        # String aleatória para usar o split
        self.SEPARATOR = "αβήταGreΕεekalphaΣσςbet.svg"
        self.name = ''
        self.ip = ''
        self.port = 0
        self.Entered = False
        self.server_address = server_address

        self.file_id = 0

        self.entry()

    def entry(self):
        Intro = tkinter.Tk()
        Intro.title("Login")
        Intro.geometry("300x400")

        nickname_entry = Entry(Intro)
        nickname_label = tkinter.Label(Intro, text="Nickname:", bg="lightgray")

        ip_entry = Entry(Intro)
        ip_label = tkinter.Label(Intro, text="IP:", bg="lightgray")

        port_entry = Entry(Intro)
        port_label = tkinter.Label(Intro, text="Port:", bg="lightgray")

        def Enter():
            # Guarda os inputs
            self.name = nickname_entry.get()
            self.ip = ip_entry.get()
            self.port = port_entry.get()

            # Manda seu endereço para o server e aguarda o endereço da outra pessoa
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect(self.server_address)

            self.udp_socket = socket(AF_INET, SOCK_DGRAM)
            self.udp_socket.bind((self.ip, int(self.port)))
            
            self.socket.send(
                (f'{self.name}{self.SEPARATOR}{self.ip}{self.SEPARATOR}{self.port}').encode())

            connection_starter, self.other_name, self.other_ip, self.other_port = self.socket.recv(
                self.BUFFER).decode().split(self.SEPARATOR)

            self.socket.close()

            # Inicia a conexão com a outra parte
            # Existe uma diferença dependendo de qual parte irá fazer o bind/listen, o que é determinado pelo parametro connection_starter
            if (connection_starter == "1"):
                p2p_socket = socket(AF_INET, SOCK_STREAM)
                p2p_socket.bind((self.ip, int(self.port)))
                p2p_socket.listen(1)
                self.connection_socket, address = p2p_socket.accept()

            else:
                self.connection_socket = socket(AF_INET, SOCK_STREAM)
                sleep(0.5)
                self.connection_socket.connect((self.other_ip, int(self.other_port)))

            self.connection_socket.send(f"oi! :) {self.other_name}".encode())

            print(self.connection_socket.recv(self.BUFFER).decode())

            # Vai para a página de chat
            Intro.destroy()
            Thread(target=self.gui_loop).start()
            Thread(target=self.receive).start()
            Thread(target=self.receive_file).start()

        nickname_label.grid(row=0, column=0, padx=5, pady=25)
        nickname_entry.grid(row=0, column=1, padx=5, pady=25)

        ip_label.grid(row=1, column=0, padx=5, pady=25)
        ip_entry.grid(row=1, column=1, padx=5, pady=25)

        port_label.grid(row=2, column=0, padx=5, pady=25)
        port_entry.grid(row=2, column=1, padx=5, pady=25)

        login_button = Button(Intro, text="Enter", command=Enter)
        login_button.grid(row=4, column=1, padx=25)
        Intro.mainloop()

    def gui_loop(self):
        self.win = tkinter.Tk()

        self.win.title(f"Chat P2P de {self.name}")
        self.win.configure(bg="lightgray")

        self.chat_label = tkinter.Label(
            self.win, text="Chat: ", bg="lightgray")
        self.chat_label.configure(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disabled")

        self.msg_label = tkinter.Label(
            self.win, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(
            self.win, text="send", command=self.write_enter)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.clear_button = tkinter.Button(
            self.win, text="Clear", command=self.clear)
        self.clear_button.config(font=("Arial", 12))
        self.clear_button.pack(padx=20, pady=5)

        self.addFile_button = tkinter.Button(
            self.win, text="Add file", command=self.UploadAction
        )
        self.addFile_button.config(font=("Arial", 12))
        self.addFile_button.pack(padx=20, pady=5)

        def clear(event):
            self.input_area.delete('1.0', 'end')
        self.input_area.bind("<Return>", self.write_enter)
        self.input_area.bind("<KeyRelease-Return>", clear)

        self.win.mainloop()

    def UploadAction(self, event=None):
        filetypes = (
            ('Video files', '*.mp4'),
            ('Photo files', '*.jpg *.jpeg *.png'),
            ('Audio files', '*.mp3*')
        )

        self.filename = filedialog.askopenfilename(
            title="Open a file",
            filetypes=filetypes
        )
        print('Selected:', self.filename)

        self.send_file()
    
    def send_file(self):
      
            with open(self.filename, "rb") as f:
                while True:
                    bytes_read =  f.read(self.BUFFER)
                    if not bytes_read:
                        break
                    self.udp_socket.sendto(bytes_read, (self.other_ip, int(self.other_port)))
            
            self.udp_socket.sendto("done".encode(),(self.other_ip, int(self.other_port)))
            print("Acabou de enviar")

       
    
    def receive_file(self):
        file_id_str = str(self.file_id)
        name = os.path.basename(self.ip + "%" +file_id_str)
        buffer_list = []
        while True:
            msg = self.udp_socket.recvfrom(self.BUFFER)
            msg = msg [0]

            if (msg == b"done"):
                break
            
            buffer_list.append(msg)
        
        self.file_id += 1
        print("Recebeu todo arquivo")
        with open(name, 'wb') as f:
           for buffer in buffer_list:
                f.write(buffer)
        Thread(target=self.receive).start()


    def write_enter(self, event=None):

        if(not self.input_area.get('1.0', 'end').strip()):
            return
        msg = f"{self.name}: {self.input_area.get('1.0', 'end')}"
        date = datetime.now()
        date = date.strftime("%d-%m-%Y %H:%Mh")
        message = f"{msg}  enviado {date}\n"
        self.input_area.delete('1.0', 'end')
        self.text_area.config(state='normal')
        self.text_area.insert('end', message)
        self.connection_socket.send(f"{msg}".encode())
        self.text_area.yview('end')
        self.text_area.config(state='disabled')
        self.Entered = True

    def clear(self):
        self.text_area.configure(state='normal')
        self.text_area.delete('1.0', 'end')
        self.text_area.configure(state='disabled')

    def receive(self):
        while True:
            msg = self.connection_socket.recv(self.BUFFER)
        
            msg = msg.decode()
            date = datetime.now()
            date = date.strftime("%d-%m-%Y %H:%Mh")
            msg = f"{msg} recebido {date}\n"
            self.text_area.config(state='normal')
            self.text_area.insert('end', msg)
            self.text_area.yview('end')
            self.text_area.config(state='disabled')
            self.Entered = True
        

        
