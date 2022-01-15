import socket

IP_ADDRS = '127.0.0.1'
PORT_NUM = 2121
FULL_ADDRS = (IP_ADDRS, PORT_NUM)
PACKET_SIZE = 1024

FTP_COMMANDS = {'OPTS': b'202 Command not implemented.\r\n', 
                'USER': b'331 User name okay, need password.\r\n',
                'PASS': b'230 Login Successful.\r\n',
                'PORT': b'200 Connected.\r\n',
                'QUIT': b'200 Goodbye.\r\n',
                 }

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

print('Starting up on {} port {}'.format(*FULL_ADDRS))

server_sock.bind(FULL_ADDRS)
server_sock.listen(1)

print('Waiting for client...')

connection_socket, client_addr = server_sock.accept()

print('Client connected from', client_addr)

connection_socket.send('220 Service ready.\r\n'.encode())

message = connection_socket.recv(PACKET_SIZE)
print('Received Message:', message)

connection_socket.send('202 UTF8 enabled.\r\n'.encode())

message = connection_socket.recv(PACKET_SIZE)
print('Received Message:', message)

connection_socket.send('331 User name okay, need password.\r\n'.encode())

message = connection_socket.recv(PACKET_SIZE)
print('Received Message:', message)

connection_socket.send('230 Login Successful.\r\n'.encode())

message = connection_socket.recv(PACKET_SIZE)
print('Received Message:', message)

connection_socket.close()