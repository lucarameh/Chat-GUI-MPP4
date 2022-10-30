from distutils.file_util import write_file
from fileinput import filename
from importlib.util import set_loader
from re import I
import tkinter
import tkinter.scrolledtext
from tkinter import INSERT, Button, Entry, simpledialog, filedialog
from datetime import datetime
from socket import *
from turtle import position
from tkVideoPlayer import TkinterVideo
from PIL import Image, ImageTk, ImageFile
from time import *
from threading import *
import shutil
from pygame import mixer
from playsound import playsound
import os

class Client:
    def __init__(self, server_address):
        self.BUFFER = 4096
        self.is_playing = False
        # String aleatória para usar o split
        self.SEPARATOR = "αβήταGreΕεekalphaΣσςbet.svg"
        self.name = ''
        self.ip = ''
        self.port = 0
        self.Entered = False
        self.server_address = server_address

        self.file_id = -1

        self.my_images = []
        self.my_images_counter = 0

        self.entry()

    # Tela inicial onde cada cliente coloca suas informações
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

        nickname_label.grid(row=0, column=0, padx=5, pady=25)
        nickname_entry.grid(row=0, column=1, padx=5, pady=25)

        ip_label.grid(row=1, column=0, padx=5, pady=25)
        ip_entry.grid(row=1, column=1, padx=5, pady=25)

        port_label.grid(row=2, column=0, padx=5, pady=25)
        port_entry.grid(row=2, column=1, padx=5, pady=25)

        # Função chamada após o usuário colocar suas informações
        def Enter():
            # Guarda os inputs
            self.name = nickname_entry.get()
            self.ip = ip_entry.get()
            self.port = port_entry.get()

            # Manda seu endereço para o server e aguarda o endereço da outra pessoa
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect(self.server_address)
            
            self.socket.send(
                (f'{self.name}{self.SEPARATOR}{self.ip}{self.SEPARATOR}{self.port}').encode())

            connection_starter, self.other_name, self.other_ip, self.other_port = self.socket.recv(
                self.BUFFER).decode().split(self.SEPARATOR)

            self.socket.close()

            # Socket udp usado para transferência de arquivos
            self.udp_socket = socket(AF_INET, SOCK_DGRAM)
            self.udp_socket.bind((self.ip, int(self.port)))

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

            # Vai para a página de chat
            Intro.destroy()
            Thread(target=self.gui_loop).start()
            Thread(target=self.receive_msg).start()
            Thread(target=self.receive_file).start()

        login_button = Button(Intro, text="Enter", command=Enter)
        login_button.grid(row=4, column=1, padx=25)
        Intro.mainloop()

    # Parte gráfica do chat
    def gui_loop(self):
        self.button_arr = []
        self.video_arr = []

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
            self.win, text="send", command=self.send_msg)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.clear_button = tkinter.Button(
            self.win, text="Clear", command=self.clear)
        self.clear_button.config(font=("Arial", 12))
        self.clear_button.pack(padx=20, pady=5)

        self.addFile_button = tkinter.Button(
            self.win, text="Add file", command=self.send_file)

        self.addFile_button.config(font=("Arial", 12))
        self.addFile_button.pack(padx=20, pady=5)

        def clear(event):
            self.input_area.delete('1.0', 'end')
        self.input_area.bind("<Return>", self.send_msg)
        self.input_area.bind("<KeyRelease-Return>", clear)

        self.win.mainloop()

    # Função para receber uma mensagem de texto
    def receive_msg(self):
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

    # Função para enviar uma mensagem de texto
    def send_msg(self, event=None):
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

    # Função para enviar um arquivo
    def send_file(self):
        # Seleciona um arquivo local e formata o nome com o qual ele será salvo
        filetypes = (
        ('Video files', '*.mp4'),
        ('Photo files', '*.jpg *.jpeg *.png'),
        ('Audio files', '*.mp3*')
        )

        self.filename = filedialog.askopenfilename(
            title="Open a file",
            filetypes=filetypes
        )
        
        _, file_type =  os.path.splitext(self.filename)
        self.udp_socket.sendto(file_type.encode(), (self.other_ip, int(self.other_port)))

        msg = f"{self.name}:"
        date = datetime.now()
        date = date.strftime("%d-%m-%Y %H:%Mh")
        message = f"{msg} enviado {date}\n"
        self.text_area.config(state='normal')
        self.text_area.insert('end', message)

        # Mostra o arquivo no chat, porém a forma como isso é feito depende do tipo dele
        if (file_type == ".png" or file_type == ".jpg" or file_type == ".jpeg"):
            img = (Image.open(self.filename)).resize((150,150))
            img = ImageTk.PhotoImage(img)
            self.my_images.append(img)

            self.text_area.image_create('end', padx=5, pady=5, image = self.my_images[len(self.my_images) - 1])
        
        elif (file_type == ".mp3"):
            
            audio_button = Button(self.text_area, text="Start audio", command= lambda filename= self.filename: self.play_mp3(filename), width=10, height=5)
            stop_button = Button(self.text_area, text="Play/Pause", command= lambda filename= self.filename: self.stop_playing(), width=10, height=5)
            self.button_arr.append(audio_button)
            self.button_arr.append(stop_button)
            
            self.text_area.window_create("end", window=self.button_arr[len(self.button_arr) -2])
            self.text_area.window_create("end", window=self.button_arr[len(self.button_arr) -1])
        
        elif (file_type == ".mp4"):
            video =  TkinterVideo(self.text_area, scaled=True)
            video.load(self.filename)
            video.pack(expand=True, fill="both")
            video.play()

            self.video_arr.append(video)
            self.text_area.window_create("end", window=self.video_arr[len(self.video_arr) - 1])

            video_button = Button(self.text_area, text="Play/Pause", command= lambda video_id= len(self.video_arr) - 1: self.play_video(video_id), width=10, height=5)
            self.button_arr.append(video_button)
            self.text_area.window_create("end", window=self.button_arr[len(self.button_arr) -1])

        self.text_area.insert('end', '\n')
        self.text_area.yview('end')
        self.text_area.config(state='disabled')

        # Começa de fato a enviar o arquivo para a outra parte
        with open(self.filename, "rb") as f:
            while True:
                bytes_read =  f.read(self.BUFFER)
                if not bytes_read:
                    break
                self.udp_socket.sendto(bytes_read, (self.other_ip, int(self.other_port)))
        
        # Mensagem de término do envio
        self.udp_socket.sendto("done".encode(),(self.other_ip, int(self.other_port)))

    # Função para receber um arquivo
    def receive_file(self):
        # Formata o nome com qual o arquivo será salvo
        file_id_str = str(self.file_id)
        file_type = self.udp_socket.recvfrom(self.BUFFER)[0].decode()
        name = os.path.basename(self.other_name + "%" +file_id_str + "." + file_type)
        buffer_list = []

        # Começa a receber as partes do arquivo e as guarda num array
        while True:
            msg = self.udp_socket.recvfrom(self.BUFFER)
            msg = msg [0]

            if (msg == b"done"):
                break
            
            buffer_list.append(msg)
        
        self.file_id += 1

        # Remonta o arquivo recebido
        with open(name, 'wb') as f:
            for buffer in buffer_list:
                f.write(buffer)

            date = datetime.now()
            date = date.strftime("%d-%m-%Y %H:%Mh")
            msg = f"{self.other_name}: recebido {date}\n"
            self.text_area.config(state='normal')
            self.text_area.insert('end', msg)

            # Mostra o arquivo no chat dependendo de seu tipo
            if (file_type == ".png" or file_type == ".jpg" or file_type == ".jpeg"):
                ImageFile.LOAD_TRUNCATED_IMAGES = True
                img = (Image.open(name)).resize((150,150))
                img = ImageTk.PhotoImage(img)
                self.my_images.append(img)
                self.text_area.image_create('end', padx=5, pady=5, image = self.my_images[len(self.my_images) - 1])
                
            
            elif (file_type == ".mp3"):
                audio_button = Button(self.text_area, text="Start audio", command= lambda filename= name: self.play_mp3(filename), width=10, height=5)
                stop_button = Button(self.text_area, text="Play/Pause", command= lambda filename= name: self.stop_playing(), width=10, height=5)
                self.button_arr.append(audio_button)
                self.button_arr.append(stop_button)
                
                self.text_area.window_create("end", window=self.button_arr[len(self.button_arr) -2])
                self.text_area.window_create("end", window=self.button_arr[len(self.button_arr) -1])
            
            elif (file_type == ".mp4"):
                video =  TkinterVideo(self.text_area, scaled=True)
                video.load(name)
                print("entrou de mp4")
                video.pack(expand=True, fill="both")
                video.play()

                self.video_arr.append(video)
                self.text_area.window_create("end", window=self.video_arr[len(self.video_arr) - 1])

                video_button = Button(self.text_area, text="Play/Pause", command= lambda video_id= len(self.video_arr) - 1: self.play_video(video_id), width=10, height=5)
                self.button_arr.append(video_button)
                self.text_area.window_create("end", window=self.button_arr[len(self.button_arr) -1])

            self.text_area.insert('end', '\n')
            self.text_area.yview('end')
            self.text_area.config(state='disabled')

        Thread(target=self.receive_file).start()

    # Limpa o chat
    def clear(self):
        self.text_area.configure(state='normal')
        self.text_area.delete('1.0', 'end')
        self.text_area.configure(state='disabled')
    
    # Função de play/pause do vídeo
    def play_video(self, video_id):
        if (self.video_arr[video_id].is_paused()):
            self.video_arr[video_id].play()
        else:
            self.video_arr[video_id].pause()
    
    # Função para iniciar o áudio
    def play_mp3(self, filename):
        mixer.init()
        mixer.music.load(filename)
        mixer.music.play()
    
    # Função de play/pause do áudio
    def stop_playing(self):
        if (mixer.music.get_busy()):
            mixer.music.pause()
        else:
            mixer.music.unpause()