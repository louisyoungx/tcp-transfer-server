import socket
import datetime

from Config import config

ADDRESS = config.Project.server_host
DEBUG_PORT = config.Project.debug_port
ALLOW = config.Project.allow_host

def handleSend(client):
    while True:
        try:  # recieving valid messages from client
            message = client.recv(1024)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'Time: {now}')
            print(f'Code: \n{message}')
            print(f'Data: \n{message.decode()}')
        except:
            client.close()
            print("====== Send Close ======")
            print('Send Closed')
            break

def track():  # accepting multiple receivers
    global receivers
    receivers = []
    print("====== Server {} Start ======".format(DEBUG_PORT))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
    server.bind((ADDRESS, DEBUG_PORT))  # binding limit and DEBUG_PORT to socket
    server.listen()
    client, ADDRESS = server.accept()
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