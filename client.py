from importlib.util import set_loader
import tkinter
import tkinter.scrolledtext
from tkinter import Button, Entry, simpledialog
from socket import *
from time import *

class Client:
    def __init__(self, server_address):
       self.BUFFER = 4096
       self.SEPARATOR = "αβήταGreΕεekalphaΣσςbet.svg" # String aleatória para usar o split
       self.name = ''
       self.ip = ''
       self.port = 0
       self.Entered = False
       self.server_address = server_address

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

            self.socket.send((f'{self.name}').encode())

            connection_starter, self.other_name, other_ip, other_port = self.socket.recv(self.BUFFER).decode().split(self.SEPARATOR)

            self.socket.close()

            # Inicia a conexão com a outra parte
            # Existe uma diferença dependendo de qual parte irá fazer o bind/listen, o que é determinado pelo parametro connection_starter
            if (connection_starter == "1"):
                print("caiu aqui")
                p2p_socket = socket(AF_INET, SOCK_STREAM)
                p2p_socket.bind((self.ip, int(self.port)))
                p2p_socket.listen(1)

                self.connection_socket, address = p2p_socket.accept()
                print("caiu aqui2")

            else:
                self.connection_socket = socket(AF_INET, SOCK_STREAM)
                sleep(0.5)
                print("caiu lá")
                self.connection_socket.connect((other_ip, int(other_port)))
            
            self.connection_socket.send(f"oi! :)".encode())

            print(self.connection_socket.recv(self.BUFFER).decode())

            # Vai para a página de chat
            Intro.destroy()
            self.gui_loop()

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

        self.chat_label = tkinter.Label(self.win, text="Chat: ", bg="lightgray")
        self.chat_label.configure(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disabled")

        self.msg_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.clear_button = tkinter.Button(self.win, text="Clear", command=self.clear)
        self.clear_button.config(font=("Arial", 12))
        self.clear_button.pack(padx=20, pady=5)

        def clear(event):
            self.input_area.delete('1.0', 'end')        
        self.input_area.bind("<Return>", self.write_enter)
        self.input_area.bind("<KeyRelease-Return>", clear)

        self.win.mainloop()

    def write(self):

        if(not self.input_area.get('1.0', 'end').strip()):
            return

        message = f"{self.name}: {self.input_area.get('1.0', 'end')}"
        self.input_area.delete('1.0', 'end')
        self.text_area.config(state='normal')
        self.text_area.insert('end', message)
        self.text_area.yview('end')
        self.text_area.config(state='disabled')

    def write_enter(self, event):

        if(not self.input_area.get('1.0', 'end').strip()):
            return

        message = f"{self.name}: {self.input_area.get('1.0', 'end')}"
        self.input_area.delete('1.0', 'end')
        self.text_area.config(state='normal')
        self.text_area.insert('end', message)
        self.text_area.yview('end')
        self.text_area.config(state='disabled')
        self.Entered = True
    
    def clear(self):
        self.text_area.configure(state='normal')
        self.text_area.delete('1.0', 'end')
        self.text_area.configure(state='disabled')

     