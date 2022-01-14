import socket

IP_ADDRS = '127.0.0.1'
PORT_NUM = 50500
FULL_ADDRS = (IP_ADDRS, PORT_NUM)
PACKET_SIZE = 1024

def messageParser(message):
    ''''''
    decoded_msg = message.decode()
    lines = decoded_msg.split('\n')
    
    request_line = lines[0]
    [method, url, version] = request_line.split(' ')

    print('Method:', method)
    print('URL:', url)
    print('Version:', version)
    

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

print('Starting up on {} port {}'.format(*FULL_ADDRS))

server_sock.bind(FULL_ADDRS)
server_sock.listen(1)

print('Waiting for client...')

connection_socket, client_addr = server_sock.accept()

print('Client connected from', client_addr)

message = connection_socket.recv(PACKET_SIZE)
messageParser(message)

#print('Request received:', message.decode(), sep='\n\n')

connection_socket.send('HTTP/1.0 200 OK\r\n\r\n<html></html><head></head><body>OK 200</body>'.encode())