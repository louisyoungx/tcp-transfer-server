import socket, threading

port = 12000
server_host = "0.0.0.0"

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

if __name__ == '__main__':
    run()
