import socket   
import threading
from tkinter import *

host = '127.0.0.1'
port = 5101
#tag = ""
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#----------------Interfaz-----------------
view = Tk()
textTag = StringVar()
mainView = Tk
textMessage = StringVar()
textHistory = StringVar()
#------------------------------------------

def initMainView():
    print("entramos a construir la vista principal")
    mainView = Tk()
    mainView.title("Cliente de socket In")
    mainView.geometry("1200x600+400+200")
    mainView.resizable(False, False)
    frame = Frame(height=500, width=1150)
    frame.grid_propagate(False)
    frame.pack(expand=1)

    labelTitle = Label(frame, text="Cliente de mensajeria por sockets ¯\_(o_O)_/¯", fg="Blue",
                       font=("Aero", 20), anchor="w")
    labelTitle.place(relx=0.0, rely=0.0)
    labelIntroduceMessage = Label(frame, text="Ingrese un mensaje aqui abajito, no sea rata", fg="Blue",
                       font=("Aero", 15), anchor="w", pady=20)
    labelIntroduceMessage.place(relx=0.0, rely=0.1)
    textFieldMessage = Entry(frame, textvariable=textMessage, font=("Aero", 15))
    textFieldMessage.place(relx=0.0, rely=0.25, relheight=0.1, relwidth=0.7)

    buttonSend = Button(frame, text="Enviar", bg="green", fg="white", font=("Aero", 15),
                        command=lambda: print("ah bueno pa saber"))
    buttonSend.place(relx=0.8, rely=0.25, relheight=0.1, relwidth=0.1)
    labelHistory = Label(frame, text="Mensajes provenientes (o que le ponemos? como historial de mensajes?) mejor el escudo de millos: ))°°//M((", fg="Blue",
                       font=("Aero", 14), anchor="w")
    labelHistory.place(relx=0.0, rely=0.4, relwidth=1)
    textFieldHistory = Label(frame, textvariable=textHistory, font=("Aero", 15), bg="white", anchor="nw",
                             justify="left")
    textFieldHistory.place(relx=0.0, rely=0.5, relheight=0.5, relwidth=1)

def startConection(tag):

    client.connect((host, port))
    receive_thread = threading.Thread(target=receive_messages, args=(tag,))
    receive_thread.start()

    write_thread = threading.Thread(target=write_messages)
    write_thread.start()
    initMainView()

def receive_messages(tag):
    while True:
        message = client.recv(1024).decode('utf-8')
        if message == "@id":
            client.send(tag.encode("utf-8"))
        else:
            print(f"server says: {message}")

def write_messages():
    message = ""
    while message.lower().strip() != 'bye':
        message = input('')
        client.send(message.encode('utf-8'))

    client.close()
    print("Client Disconnected")

def setTag(tagIn):
    #tag = tagIn
    view.destroy()
    startConection(tagIn)


def initView(view, textTag):
    view.title("Cliente de socket")
    view.geometry("400x300+400+200")
    view.resizable(False, False)

    frame = Frame(height=300, width=400)
    frame.grid_propagate(False)
    frame.pack(expand=1)

    labelTitle = Label(frame, text="Servidor de sockets, bienvenido", fg="Blue",
                       font=("Aero", 18), anchor="n", justify=CENTER, pady=20)
    labelTitle.place(relx=0.0, rely=0.1, relwidth=1)

    labelIntroduceTag = Label(frame, text="Introduzca un tag", fg="Blue",
                       font=("Aero", 15), anchor="n", justify=CENTER, pady=20)
    labelIntroduceTag.place(relx=0.0, rely=0.3, relwidth=1)

    textFieldTag = Entry(frame, textvariable=textTag, font=("Aero", 14))
    textFieldTag.place(relx=0.1, rely=0.5, relheight=0.15, relwidth=0.8)

    buttonSend = Button(frame, text="Enviar", bg="green", fg="white", font=("Aero", 15),
                        command=lambda: setTag(textTag.get()))
    buttonSend.place(relx=0.25, rely=0.7, relheight=0.15, relwidth=0.5)

#-------------Al final-------------------
    view.mainloop()

initView(view, textTag)

"""
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=write_messages)
write_thread.start()
"""