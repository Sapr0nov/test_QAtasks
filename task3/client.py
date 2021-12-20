import socket
import threading

HOST = '127.0.0.1'
PORT_Auth = 8000
PORT_msg = 8001

client_id = ''


def read_so():
    global client_id

    while True:
        data = so.recv(1024)
        print('response server: ' + data.decode('utf-8'))

        if data.decode('utf-8') == '200':
            client_id = input('Choice your id: ')
            so.sendto(client_id.encode('utf-8'), server_Auth)


server_Auth = HOST, PORT_Auth

so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
so.bind(('', 0))

client_id = input('Choice your id: ')
so.sendto(client_id.encode('utf-8'), server_Auth)

thread = threading.Thread(target=read_so)
thread.start()

while True:
    msg = input(client_id + ' enter msg: ')
    print(msg)
    so.sendto(('[' + client_id + ']' + msg).encode('utf-8'), server_Auth) # server_msg
