import socket
import sys

HOST = ''
PORT = 50000
BACKLOG = 5
SIZE = 1024

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
except (socket.error , msg):
    print('Failed to create socket. Error code: ' + str(msg[0]))
    print('Error message: ' + msg[1])
    sys.exit()
print('Socked created and binding complete')

s.listen(BACKLOG)
print('Server listening')

while 1:
    (conn, addr) = s.accept()
    # print('Connected with ' + addr[0] + ':' + str(addr[1]))

    data = conn.recv(1024)
    print(data)
    reply = 'OK...' + data
    if data:
        conn.send(reply)
    conn.close()
s.close()
