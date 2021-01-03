import socket
import base64
import hashlib
from Settings import port, allow_host
from Utils import get_headers, send_msg


def run():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((allow_host, port))
    server.listen(5)
    print("The TCP Server in {} Start".format(port))

    client, address = server.accept()
    data = client.recv(1024)
    print(data.decode())
    headers = get_headers(data)
    response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
                   "Upgrade:websocket\r\n" \
                   "Connection:Upgrade\r\n" \
                   "Sec-Core-Accept:%s\r\n" \
                   "Core-Location:ws://%s%s\r\n\r\n"

    value = headers['Sec-Core-Key'] + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    ac = base64.b64encode(hashlib.sha1(value.encode('utf-8')).digest())
    response_str = response_tpl % (ac.decode('utf-8'), headers['Host'], headers['url'])
    print(response_str)
    client.send(bytes(response_str, encoding='utf-8'))

    while True:
        try:
            info = client.recv(8096)
        except Exception as e:
            info = None
        if not info:
            break
        payload_len = info[1] & 127
        if payload_len == 126:
            extend_payload_len = info[2:4]
            mask = info[4:8]
            decoded = info[8:]
        elif payload_len == 127:
            extend_payload_len = info[2:10]
            mask = info[10:14]
            decoded = info[14:]
        else:
            extend_payload_len = None
            mask = info[2:6]
            decoded = info[6:]

        bytes_list = bytearray()
        for i in range(len(decoded)):
            chunk = decoded[i] ^ mask[i % 4]
            bytes_list.append(chunk)
        body = str(bytes_list, encoding='utf-8')
        print(body)
        send_msg(client, "OK".encode())

    server.close()