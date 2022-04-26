import socket
import threading
import datetime

from Core.WebSocket.WebSocket import WebSocket
from Settings import debug_port as port

def handleSend(client):
    while True:
        try:  # recieving valid messages from client
            message = client.recv(1024).decode()
            now = datetime.datetime.now ().strftime('%Y-%m-%d %H:%M:%S')
            print(f'{now} - {message}')
        except:
            client.close()
            print("====== Send Close ======")
            print('Send Closed')
            break

def track():  # accepting multiple receivers
    allow = ''  # LocalHost
    global receivers
    receivers = []
    print("====== Server {} Start ======".format(port))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
    server.bind((allow, port))  # binding limit and port to socket
    server.listen()
    client, address = server.accept()
    key = client.recv(1024)
    try:
        value = key.decode()
        print(value)
    except:
        print(f'ERROR MESSAGE: {key}')
        value = ""
    print("====== Send Connection Built ======")
    client.send('Success'.encode())
    handleSend(client)