import socket

IP_ADDRS = '127.0.0.1'
PORT_NUM = 2121
FULL_ADDRS = (IP_ADDRS, PORT_NUM)
PACKET_SIZE = 1024

def client_connected_handler():
    return '220 Service ready.\r\n'

def command_parser(message):
    
    message_parts = message.split(' ')
    ftp_command = message_parts[0].strip()
    return ftp_command

def opts_command_handler():
    return '202 Command not implemented.\r\n'

def user_command_handler():
    return '331 User name okay, need password.\r\n'

def pass_command_handler():
    return '230 Login Successful.\r\n'
    
def port_command_handler():
    return '200 Connected.\r\n'
    
def quit_command_handler():
    return '200 Goodbye.\r\n'
    

FTP_COMMANDS = {'OPTS': opts_command_handler, 
                'USER': user_command_handler,
                'PASS': pass_command_handler,
                'PORT': port_command_handler,
                'QUIT': quit_command_handler,
                 }

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

print('Starting up on {} port {}'.format(*FULL_ADDRS))

server_sock.bind(FULL_ADDRS)
server_sock.listen(1)

print('Waiting for client...')

connection_socket, client_addr = server_sock.accept()

print('Client connected from', client_addr)

connection_socket.send(client_connected_handler().encode())

function_handler = None

while function_handler != FTP_COMMANDS['QUIT']:
    message = connection_socket.recv(PACKET_SIZE)
    print('Received Message:', message)
    function_handler = FTP_COMMANDS[command_parser(message.decode())]
    response = function_handler()
    connection_socket.send(response.encode())

connection_socket.close()