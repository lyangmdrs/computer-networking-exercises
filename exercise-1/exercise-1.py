import socket

IP_ADDRS = '127.0.0.1'
PORT_NUM = 50500
FULL_ADDRS = (IP_ADDRS, PORT_NUM)
PACKET_SIZE = 1024
OBJ_TAG = '<object data="{}"></object>'
MSG_TAG = '<h3>{} - {}</h3>'
HTML_PAGE = '<html><head><h1>Exercise 1</h1></head><body><h3>{} - {}</h3><object data="{}"></object></body></html>'

def messageParser(message):
    ''''''
    lines = message.splitlines()
    
    request_line = lines[0]
    [method, url, version] = request_line.split(' ')

    print('Method:', method)
    print('URL:', url)
    print('Version:', version)
    
    if method != 'GET':
        return ('501', 'Not Implemented', version, '')
    
    if url == '/':
        print('Root path request!')
        return('200', 'OK', version, '')

    file_name = url.replace('/', '')
    print('Requesting the file:', file_name)

    try:
        with open(file_name) as f:
            f.close()
            pass

    except IOError:
        print('The file "{}" was not found!'.format(file_name))
        return('404', 'Not Found', version, '')

    else:
        print('The file "{}" is present!'.format(file_name))
        return('200', 'OK', version, file_name)


server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

print('Starting up on {} port {}'.format(*FULL_ADDRS))

server_sock.bind(FULL_ADDRS)
server_sock.listen(1)

print('Waiting for client...')

connection_socket, client_addr = server_sock.accept()

print('Client connected from', client_addr)

message = connection_socket.recv(PACKET_SIZE)

(status_code, status_msg, version, file_name) = messageParser(message.decode())

status_line = '{} {} {}\n'.format(version, status_code, status_msg)
header_line = ''
blank_line = '\n'

body = HTML_PAGE.format(status_code, status_msg, file_name)

response_message = status_line + header_line + blank_line + body

connection_socket.send(response_message.encode())