from email import message
import socket   
import threading

host = '127.0.0.1'
port = 5101

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
            print(f"{tag} is offline")
            break
        print(f"{tag} says: {message}")

def broadcast(message):
    for client in clients:
        client.send(message.encode("utf-8"))

def write_messages():
    while True:
        message = input('')
        broadcast(message)

def receive_connections():
    while True:
        client, address = server.accept()
        client.send("@id".encode("utf-8"))
        tag = client.recv(1024).decode('utf-8')
        clients.append(client)
        tags.append(tag)

        print(f"{tag} is connected with {str(address)}")
        client.send("Connected to server".encode("utf-8"))


        thread = threading.Thread(target=show_messages, args=(client,))
        thread.start()

        thread = threading.Thread(target=write_messages)
        thread.start()

receive_connections()