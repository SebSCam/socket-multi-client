import socket   
import threading

tag = input("Enter a tag to Client: ")

host = '127.0.0.1'
port = 5102

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


def receive_messages():
    message = ''
    while message.lower().strip() != 'bye':
        message = client.recv(1024).decode('utf-8')
        if message == "@id":
            client.send(tag.encode("utf-8"))
        else:
            print(message)

    print("Server finished all connections")
    client.close()

def write_messages():
    while True:
        message = input('')
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=write_messages)
write_thread.start()