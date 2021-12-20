import socket

HOST = '127.0.0.1'
PORT_Auth = 8000
PORT_msg = 8001
sock_auth = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_msg = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_auth.bind((HOST, PORT_Auth))
sock_msg.bind((HOST, PORT_msg))

clients = []
clientsID = []

print('Server start listening on ' + HOST + ':' + str(PORT_Auth) + ', ' + str(PORT_msg))

while True:
#    msg, address = sock_msg.recvfrom(1024)
    data, address = sock_auth.recvfrom(1024)

    print(address[0], address[1])

    if address not in clients:
        clients.append(address)
        clientsID.append(data)
        print(data)
        print('msg: ' + str(address[0]) + ':' + str(address[1]))
        sock_auth.sendto('200'.encode('utf-8'), address)

    for client in clients:
        if client == address:
            print('msg: ' + str(client[0]) + ':' + str(client[1]))
            sock_auth.sendto('200'.encode('utf-8'), client)
            continue
        sock_auth.sendto(data, client)
