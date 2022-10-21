import socket   
import threading
from tkinter import *

host = '127.0.0.1'
port = 5101
#tag = ""
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#----------------Interfaz-----------------

view = Tk()
textHistory = StringVar()
#textHistory = StringVar()
#textHistory.set("Historial")
textTag = StringVar()

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

    labelTitle = Label(frame, text="Cliente de mensajeria por sockets", fg="Blue",
                       font=("Aero", 20), anchor="w")
    labelTitle.place(relx=0.0, rely=0.0)
    labelIntroduceMessage = Label(frame, text="Ingrese un mensaje", fg="Blue",
                       font=("Aero", 15), anchor="w", pady=20)
    labelIntroduceMessage.place(relx=0.0, rely=0.1)
    textMessage = StringVar()
    textFieldMessage = Entry(frame, textvariable=textMessage, font=("Aero", 15))
    textFieldMessage.place(relx=0.0, rely=0.25, relheight=0.1, relwidth=0.7)

    buttonSend = Button(frame, text="Enviar", bg="green", fg="white", font=("Aero", 15),
                        command=lambda: write_messages(textMessage.get()))
    buttonSend.place(relx=0.8, rely=0.25, relheight=0.1, relwidth=0.1)
    labelHistory = Label(frame, text="Historial de mensajes", fg="Blue",
                       font=("Aero", 14), anchor="w")
    labelHistory.place(relx=0.0, rely=0.4, relwidth=1)
    textHistory.set("Historial")
    textFieldHistory = Label(frame, textvariable=textHistory, font=("Aero", 15), bg="white", anchor="nw",
                             justify="left")
    textFieldHistory.place(relx=0.0, rely=0.5, relheight=0.5, relwidth=1)
    mainView.mainloop()
def startConection(tag):

    client.connect((host, port))
    receive_thread = threading.Thread(target=receive_messages, args=(tag,))
    receive_thread.start()

    #write_thread = threading.Thread(target=write_messages)
    #write_thread.start()
    initMainView()

def receive_messages(tag):
    while True:
        message = client.recv(1024).decode('utf-8')
        if message == "@id":
            client.send(tag.encode("utf-8"))
        else:
            #textHistory.set("porty")
            print(f"server says: {message}")

def write_messages(message):
    if message.lower().strip() != 'bye':
        client.send(message.encode('utf-8'))
    else:
        client.close()
        print("Client Disconnected")

def setTag(tagIn):
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