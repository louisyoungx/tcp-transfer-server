import socket, threading

from Settings import port, server_host


def run():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
    client.connect((server_host, port))  # connecting client to server
    client.send("Send".encode())
    print("start --- >")

    def write():
        while True:  # message layout
            message = '{}'.format(input(''))
            client.send(message.encode())

    write_thread = threading.Thread(target=write)  # sending messages
    write_thread.start()
