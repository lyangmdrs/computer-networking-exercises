import socket

IP_ADDRS = '127.0.0.1'
PORT_NUM = 50500
FULL_ADDRS = (IP_ADDRS, PORT_NUM)
PACKET_SIZE = 1024

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

print('Starting up on {} port {}'.format(*FULL_ADDRS))

server_sock.bind(FULL_ADDRS)
server_sock.listen(1)

print('Waiting for client...')

connectionSocket, client_addr = server_sock.accept()

print('Client connected from', client_addr)

message = connectionSocket.recv(PACKET_SIZE)

print('Request received:', message.decode(), sep='\n\n')