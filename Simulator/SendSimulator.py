import csv
import socket, threading
from time import sleep

port = 12000
server_host = "0.0.0.0"
simu_data = "simu_data.csv"

def readData():
    with open(simu_data, "r", encoding='UTF-8') as file:
        data = csv.reader(file)
        lst = []
        for row in data:
            try:
                lst.append(row[0])
            except:
                pass
    return lst

def run():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
    client.connect((server_host, port))  # connecting client to server
    client.send("Send".encode())
    print("start --- >")
    def write():
        data = readData()
        index = 0
        step = 10
        while True:  # message layout
            message = data[index]
            print(message)
            if index >= len(data) - 1 - step:
                index = 0
            else:
                index += step
            client.send(message.encode())
            sleep(0.1)

    write_thread = threading.Thread(target=write)  # sending messages
    write_thread.start()

if __name__ == '__main__':
    run()