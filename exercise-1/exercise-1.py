import socket

IP_ADDRS = '127.0.0.1'
PORT_NUM = 50500
FULL_ADDRS = (IP_ADDRS, PORT_NUM)
PACKET_SIZE = 1024

def messageParser(message):
    ''''''
    lines = message.split('\n')
    
    request_line = lines[0]
    [method, url, version] = request_line.split(' ')

    print('Method:', method)
    print('URL:', url)
    print('Version:', version)
    
    if method != 'GET':
        return (501, 'Not Implemented', version)
    
    return(200, 'OK', version)

def getHtmlContent():
    html_content = ''
    with open('responseMessage.html') as response_message_file:
        html_content = response_message_file.read()
    return html_content

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

print('Starting up on {} port {}'.format(*FULL_ADDRS))

server_sock.bind(FULL_ADDRS)
server_sock.listen(1)

print('Waiting for client...')

connection_socket, client_addr = server_sock.accept()

print('Client connected from', client_addr)

message = connection_socket.recv(PACKET_SIZE)

print('Request received:', message.decode(), sep='\n\n')

(status_code, status_msg, version) = messageParser(message.decode())

status_line = '{} {} {}\n'.format(version, status_code, status_msg)
header_line = ''
blank_line = '\n'
body = getHtmlContent()

response_message = status_line + header_line + blank_line + body

connection_socket.send(response_message.encode())