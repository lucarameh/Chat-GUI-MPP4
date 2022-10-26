from importlib.util import set_loader
import tkinter
import tkinter.scrolledtext
from tkinter import Button, Entry, simpledialog

class Client:

    def entry(self):
       Intro = tkinter.Tk()
       Intro.title("Login")
       Intro.geometry("300x400")

       nickname_entry = Entry(Intro)
       ip_entry = Entry(Intro)
       port_entry = Entry(Intro)
       

       def Enter():
         self.name = nickname_entry.get()
         self.ip = ip_entry.get()
         self.port = port_entry.get()
         Intro.destroy()

       nickname_entry.grid(row=0, column=0, pady = 30, padx = 90)
       ip_entry.grid(row=1, column=0, pady = 30, padx = 5)
       port_entry.grid(row=2, column=0, pady = 30, padx = 5)
       
       login_button = Button(Intro, text="Enter", command=Enter)
       login_button.grid(row=3, column=0, pady = 30, padx = 5)
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

    def __init__(self):
       self.name = ''
       self.ip = ''
       self.port = 0
       self.Entered = False
       self.entry()
       self.gui_loop()

       
      
client = Client()