import socket

HOST = '127.0.0.1'
PORT_auth = 8000
PORT_msg = 8001
auth_code = ''
client_id = ''

so_auth = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so_msg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so_auth.connect((HOST, PORT_auth))
so_msg.connect((HOST, PORT_msg))

while True:

    if auth_code == '':
        msg = input('Choice your clientID: ')
        so_auth.sendall(msg.encode("utf-8"))
        data = so_auth.recv(1024)
        client_id = msg

        if data.decode('utf-8') == 'err':
            print('Please choice another clientID')
            client_id = ''
        else:
            auth_code = data.decode('utf-8')
            print('Your get auth code')

    else:
        msg = input('send message: ')
        so_msg.sendall((client_id + '@@' + auth_code + '@@' + msg).encode("utf-8"))
        data = so_msg.recv(1024)
        if data.decode('utf-8') == 'err':
            print('Something wrong check your ID code and message')
        else:
            print('Message save.')
