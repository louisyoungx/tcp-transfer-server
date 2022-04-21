import socket
import threading  # Libraries import

from Core.WebSocket.WebSocket import WebSocket
from Settings import port

def broadcast(message):  # broadcast function declaration
    for Receiver in receivers:
        Receiver.send(message)

def handleSend(client):
    while True:
        try:  # recieving valid messages from client
            message = client.recv(1024).decode()
            # print(message)
            broadcast(message)
        except:
            client.close()
            print("====== Send Close ======")
            broadcast('Send Closed')
            break


def handleReceive(Receiver):
    while True:
        try:  # recieving valid messages from client
            message = Receiver.client.recv(1024)
            broadcast(message)
        except:  # removing receivers
            receivers.remove(Receiver)
            Receiver.client.close()
            print("====== Receive Close ======")
            broadcast('Receive Closed')
            break

def run():  # accepting multiple receivers
    allow = ''  # LocalHost
    global receivers
    receivers = []
    print("====== Server {} Start ======".format(port))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
    server.bind((allow, port))  # binding limit and port to socket
    server.listen()
    while True:
        client, address = server.accept()
        key = client.recv(1024)
        try:
            value = key.decode()
            print(value)
        except:
            print(f'ERROR MESSAGE: {key}')
            value = ""
        if "GET / HTTP/1.1" in value:
            print("====== Receive Connection Built ======")
            try:
                Receiver = WebSocket(client)
                Receiver.init(key)
            except:
                continue
            try:
                info = client.recv(8096)
            except Exception as e:
                info = "None"
            body = Receiver.unpackage(info)
            #send_msg(client, "OK".encode())
            Receiver.send('Success')
            receivers.append(Receiver)
            broadcast("Connect Receive Server Success")
            Receive_Thread = threading.Thread(target=handleReceive, args=(Receiver,))
            Receive_Thread.start()
            continue
        else:
            print("====== Send Connection Built ======")
            broadcast("Connect Send Server Success")
            client.send('Success'.encode())
            Send_Thread = threading.Thread(target=handleSend, args=(client,))
            Send_Thread.start()