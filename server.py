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


clients = {}

def clientThread(conn):
    my_uuid = ""
    try:
        while 1:
            twoPlayerConnected = False
            data = conn.recv(SIZE)
            client = {}
            if data.startswith("M"):
                _, uuid, x, y = data.split(':')
                my_uuid = uuid
                clients[uuid] = {"x": x, "y": y}
            if len(clients) == 2:
                twoPlayerConnected = True
                for key in clients:
                    if key is not my_uuid:
                        client = clients[key]
                        data = ""
                        for pos in client:
                            data += "%s:%s:" % (pos, client[pos])
                            # print("Pos %s: %s" % (pos, client[pos]))
                        # print("Pos y: %s" % (client[y]))
                        # print("Pos x: %s" % (client[x]))
                        data = data[:-1]
            if data and twoPlayerConnected:
                conn.send(data)
            else:
                conn.send("y:142.0:x:160.0")
        conn.close()

    except Exception as e:
        print e.message

while 1:
    (conn, addr) = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    start_new_thread(clientThread ,(conn,))

s.close()
