import socket
import sys
from thread import *


HOST = ''
PORT = 50000
BACKLOG = 5
SIZE = 1024

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
except socket.error , msg:
    print('Failed to create socket. Error code: ' + str(msg[0]))
    print('Error message: ' + msg[1])
    sys.exit()
print('Socked created and binding complete')

s.listen(BACKLOG)
print('Server listening')


clients = {"other": {"x": 0, "y": 0}}

def clientThread(conn):
    try:
        while 1:
            data = conn.recv(SIZE)
            if data.startswith("M"):
                _, uuid, x, y = data.split(':')
                clients[uuid] = {"x": x, "y": y}
            if data:
                conn.send("")
        conn.close()
    except Exception as e:
        print e.message

while 1:
    (conn, addr) = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    start_new_thread(clientThread ,(conn,))

s.close()
