from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys

clients = {}
addresses = {}

HOST = 'localhost'
PORT = 5512
message_limit = 1024
host_address = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(host_address)


def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, 'utf8')+msg)


def handle_client(client):
    name = client.recv(message_limit).decode('utf8')
    # client will receive this message
    client.send(bytes(f'Welcome {name}<3', 'utf8'))
    # this will inform everyone that client has joined
    broadcast(bytes(f'{name} has joined!!', 'utf8'))
    clients[client] = name
    run = True
    try:
        while run:
            msg = client.recv(message_limit)
            if msg != bytes('{quit}', "utf8"):
                broadcast(msg, name + ": ")
            else:
                client.send(bytes('{quit}', 'utf8'))
                client.close()
                del clients[client]
                broadcast(bytes(f'{name} has left the conversation.T_T', 'utf8'))
                run = False
    except Exception as e:
        print(f'Error occured {e}')
        run = False


def accepting_incoming_connections():
    run = True
    try:
        while run:
            client, client_address = SERVER.accept()
            print(f'{client} : {client_address} has connected')
            client.send(bytes("Message recieved", "utf8"))
            addresses[client] = client_address
            Thread(target=handle_client, args=(client,)).start()
    except Exception as e:
        print(f'Error occured {e}')
        run = False
        sys.exit(0)


if __name__ == "__main__":
    SERVER.listen(10) # will listen to 10 connections
    print('Waiting for connections')
    ACCEPT_THREAD = Thread(target=accepting_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
