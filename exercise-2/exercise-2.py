import socket
from time import sleep

IP_ADDRS = '127.0.0.1'
PORT_NUM = 2121
FULL_ADDRS = (IP_ADDRS, PORT_NUM)
PACKET_SIZE = 1024

data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def client_connected_handler():
    return '220 Service ready.\r\n'

def command_parser(message):
    
    message_parts = (message.strip()).split(' ')
    ftp_command = message_parts[0]
    arguments = ' '.join(message_parts[1:])
    return (ftp_command, arguments)

def opts_command_handler(args):
    return '202 Command not implemented.\r\n'

def user_command_handler(args):
    return '331 User name okay, need password.\r\n'

def pass_command_handler(args):
    return '230 Login Successful.\r\n'
    
def port_command_handler(args):
    
    global data_sock

    args_splited = args.split(',')
    data_ip_parts = args_splited[:4]
    data_port_parts = [int(part) for part in args_splited[4:]]

    data_ip = '.'.join(data_ip_parts)
    data_port =  (data_port_parts[0] * 256) + data_port_parts[1]

    print('Data IP:', data_ip)
    print('Data port:', data_port)
    
    data_sock.connect((data_ip, data_port))

    print('Data connection successfully stablished!')

    return '200 Connected.\r\n'
    
def quit_command_handler(args):
    return '200 Goodbye.\r\n'
    

FTP_COMMANDS = {'OPTS': opts_command_handler, 
                'USER': user_command_handler,
                'PASS': pass_command_handler,
                'PORT': port_command_handler,
                'QUIT': quit_command_handler,
                 }

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Starting up on {} port {}'.format(*FULL_ADDRS))

server_sock.bind(FULL_ADDRS)
server_sock.listen(1)

print('Waiting for client...')

connection_socket, client_addr = server_sock.accept()

print('Client connected from', client_addr)

connection_socket.send(client_connected_handler().encode())

function_handler = None

while function_handler != FTP_COMMANDS['QUIT']:
    
    message = (connection_socket.recv(PACKET_SIZE)).decode()
    print('Received Message:', message.strip())
    (ftp_command, arguments) = command_parser(message)
    
    try:
        function_handler = FTP_COMMANDS[ftp_command]
    except KeyError:
        print("I don't know how to answer to this command!")
        response = '421 Service not available, closing control connection.\r\n'
        function_handler = FTP_COMMANDS['QUIT']
    else:
        response = function_handler(arguments)

    connection_socket.send(response.encode())

print('Clossing connection...')
connection_socket.close()
print('Connection closed!')