import socket
import sys

HOST = ''
PORT = 50000

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
except (socket.error , msg):
    print('Failed to create socket. Error code: ' + str(msg[0]))
    print('Error message: ' + msg[1])
    sys.exit()
print('Socked created and binding complete')
