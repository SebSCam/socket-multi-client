from email import message
import socket   
import threading
from tkinter import *
import os
import re

host = '127.0.0.1'
port = 5102

#------------------------
view = Tk()
textActivityUsers = StringVar()
textHistory = StringVar()
textMessage = StringVar()
#-------------------
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()
print(f"Server running on {host}:{port}")

clients = []
tags = []
def show_messages(client):

    while True:
        index = clients.index(client)
        tag = tags[index]
        message = client.recv(1024).decode("utf-8")
        if message.lower().strip() == 'bye':
            clients.remove(client)
            tags.remove(tag)
            textActivityUsers.set(textActivityUsers.get() + "\n" + f"{tag} is offline")
            #print(f"{tag} is offline")
            break
        textHistory.set(textHistory.get()+"\n"+f"{tag} says: {message}")
        #print(f"{tag} says: {message}")

def broadcast(message):
    for client in clients:
        client.send(message.encode("utf-8"))
    textMessage.set("")
    textHistory.set(textHistory.get() + "\n" + f"I said: {message}")

def write_messages():
    while True:
        message = input('')
        broadcast(message)

def receive_connections():
    indicator = 0
    while True:

        client, address = server.accept()
        client.send("@id".encode("utf-8"))
        tag = client.recv(1024).decode('utf-8')
        clients.append(client)
        tags.append(tag)

        #print(f"{tag} is connected with {str(address)}")
        textActivityUsers.set(textActivityUsers.get()+"\n"+f"{tag} is connected with {str(address)}")
        client.send("Connected to server".encode("utf-8"))


        thread = threading.Thread(target=show_messages, args=(client,))
        thread.start()

        thread = threading.Thread(target=write_messages)
        thread.start()

def initView(view, textActivityUsers, textHistory, textMessage):

    view.title("Servidor de socket")
    view.geometry("1200x600+400+200")
    view.resizable(False, False)

    frame = Frame(height=500, width=1150)
    frame.grid_propagate(False)
    frame.pack(expand=1)

    labelTitle = Label(frame, text="Servidor de sockets, bienvenido", fg="Blue", font=("Aero", 20), anchor="w")
    labelTitle.place(relx=0.0, rely=0.0)

    labelIntroduceMessage = Label(frame, text="Ingrese un mensaje", fg="Blue",
                       font=("Aero", 15), anchor="w", pady=20)
    labelIntroduceMessage.place(relx=0.0, rely=0.1)

    labelHistoryUsers = Label(frame, text="Actividad de los usuarios", fg="Blue",
                       font=("Aero", 15), anchor="w", pady=20)
    labelHistoryUsers.place(relx=0.7, rely=0.1)

    textFieldMessage = Entry(frame, textvariable=textMessage, font=("Aero", 15))
    textFieldMessage.place(relx=0.0, rely=0.25, relheight=0.1, relwidth=0.4)

    buttonSend = Button(frame, text="Enviar", bg="green", fg="white",font=("Aero", 15),
                          command=lambda:broadcast(textMessage.get()))
    buttonSend.place(relx=0.5, rely=0.25, relheight=0.1, relwidth=0.1)

    textFieldActivity = Label(frame, textvariable=textActivityUsers, font=("Aero", 15), bg="white",anchor="nw", justify="left")
    textFieldActivity.place(relx=0.7, rely=0.25, relheight=0.75, relwidth=0.3)


    textFieldHistory = Label(frame, textvariable=textHistory, font=("Aero", 15), bg="white",anchor="nw", justify="left")
    textFieldHistory.place(relx=0.0, rely=0.4, relheight=0.55, relwidth=0.6)
    view.mainloop()

threadConections = threading.Thread(target=receive_connections)
threadConections.start()
initView(view, textActivityUsers, textHistory, textMessage)
