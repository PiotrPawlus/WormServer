import sys
import time
import socket
from thread import *
import random


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
    try:
        while 1:
            packet = conn.recv(SIZE)

            _data = packet.split(':')
            kind = _data[0]
            uuid = _data[1]

            data = _data[2:-1]
            client_time = float(_data[-1])
            server_time = time.time()

            print "-->", packet, "ping", server_time - client_time

            back = ""

            if kind == "W":
                others = [c for c in clients.keys() if c != uuid]
                position = data
                if not others:
                    pair = None
                else:
                    pair = others[0]

                clients[uuid] = {"state": "W", "pair": pair, "position": position}

                back = "W:%d:%s:%f" % (
                    1 if pair else 0,
                    ":".join(position),
                    server_time)

            if kind == "M":
                client = clients[uuid]
                client['position'] = data

                pair = client['pair']
                pair_position = clients[pair]['position']

                back = "M:%s:%f" % (":".join(pair_position), server_time)

            if kind == "P":
                print("---------")
                print("data: %s" % data)
                client = clients[uuid]
                client_position = data[:-3]
                point_position = data[3:5]
                point_collected = data[-1]

                if point_collected is "1":
                    point_position = []
                    point_position.insert(0, random.uniform(0.0, data[6]))
                    point_position.insert(1, random.uniform(0.0, data[7]))

                pair = client['pair']
                pair_position = clients[pair]['position']

                back = "P:%s:%s:%s:%f" % (":".join(pair_position), ":".join(map(str, point_position)), point_collected ,server_time)
            if not back:
                assert "bad packet"

            print "<---", back, uuid
            conn.send(back)

        conn.close()

    except Exception as e:
        print e.message

while 1:
    (conn, addr) = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    start_new_thread(clientThread, (conn, ))


s.close()
