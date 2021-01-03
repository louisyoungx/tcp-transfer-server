import socket, threading

from Settings import port

def run():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
    client.connect(('127.0.0.1', port))  # connecting client to server
    client.send("Send".encode())
    print("start --- >")

    def write():
        while True:  # message layout
            message = '{}'.format(input(''))
            client.send(message.encode())

    write_thread = threading.Thread(target=write)  # sending messages
    write_thread.start()
