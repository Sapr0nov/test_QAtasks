import os
import csv
import types
import socket
import random
import selectors

HOST = '127.0.0.1'
PORT_auth = 8000
PORT_msg = 8001
clientsID = []  # array of array [[clientId, code], [clientId, code]]

#  logging
dir_path_self = os.path.dirname(os.path.realpath(__file__))
output_file = open(dir_path_self + '/log.csv', 'a', encoding='UTF8')
writer = csv.writer(output_file, dialect='unix')

#  connection
sel = selectors.DefaultSelector()
so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so_msg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so.bind((HOST, PORT_auth))
so_msg.bind((HOST, PORT_msg))

so.listen()
so_msg.listen()

print('listening on', (HOST, PORT_auth))
print('listening on', (HOST, PORT_msg))

so.setblocking(False)
sel.register(so, selectors.EVENT_READ, data=None)
sel.register(so_msg, selectors.EVENT_READ, data=None)

random.seed()

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print('accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def write_log(client, msg):
    row = [client, msg]
    writer.writerow(row)


def find_client(array, text):
    for client in array:
        if text in client:
            return client
    return False


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    incoming_port = sock.getsockname()[1]

    if mask & selectors.EVENT_READ:

        recv_data = sock.recv(1024)

        if recv_data:
            data.outb += bytes(recv_data)
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE:

        if data.outb:
            recv_text = data.outb.decode('utf-8')
            data.outb = bytes('', encoding='utf-8')

            if incoming_port == 8001:

                client_id, code, msg = recv_text.split("@@")
                write_log(client_id, msg)
                if find_client(clientsID, client_id)[1] == code:
                    sock.send('200 ok'.encode('utf-8'))
                    print('added new message from ', data.addr)
                else:
                    sock.send('err'.encode('utf-8'))
                    print('incorrect code', data.addr)

            if incoming_port == 8000:

                if not find_client(clientsID, recv_text):
                    code = str(random.randint(1000, 9999))
                    client = [recv_text, code]
                    clientsID.append(client)
                    sock.send(code.encode('utf-8'))
                    print('create new ClientID from', data.addr)
                else:
                    sock.send('err'.encode('utf-8'))
                    print('duplicate ClientID from', data.addr)


while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)
