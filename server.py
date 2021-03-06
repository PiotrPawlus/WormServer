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

                star = [0.0, 0.0]
                clients[uuid] = {"state": "W", "pair": pair, "position": position, "star": star}

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
                client = clients[uuid]
                client_x, client_y, client_rot, point_x, point_y, need_new_point, frame_width, frame_height = data

                client['position'] = [client_x, client_y, client_rot]
                pair = client['pair']
                pair_position = clients[pair]['position']

                if need_new_point:
                    width = random.uniform(0.0, float(frame_width))
                    height = random.uniform(0.0, float(frame_height))
                    client['star'] = [width, height, '0']
                    clients[pair]['star'] = [width, height, '0']

                back = "P:%s:%s:%f" % (":".join(pair_position), ":".join(map(str, client['star'])), server_time)
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
