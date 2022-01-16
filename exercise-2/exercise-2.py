import socket

IP_ADDRS = '127.0.0.1'
PORT_NUM = 2121
FULL_ADDRS = (IP_ADDRS, PORT_NUM)
PACKET_SIZE = 1024

# Just initializing the socket object
data_sock = socket.socket()
cmd_sock = socket.socket()

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
    
    data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_sock.connect((data_ip, data_port))

    print('Data connection successfully stablished!')

    return '200 Connected.\r\n'
    
def quit_command_handler(args):
    return '200 Goodbye.\r\n'

def retr_command_handler(args):

    file_data = b''
    try:
        with open(args, 'rb') as retr_file:
            file_data = retr_file.read()
    except FileNotFoundError:
        data_sock.close()
        return '426 Transfer aborted: Requested file is not present.\r\n'
    else:
        retr_file.close()

    cmd_sock.send('150 Starting data transfer\r\n'.encode())
    data_sock.send(file_data)
    data_sock.close()

    return '226 Operation successful\r\n'

def stor_command_handler(args):
    
    cmd_sock.send('150 Starting data transfer\r\n'.encode())
    file_data = b''
    received_data = data_sock.recv(PACKET_SIZE)

    while (received_data):
        file_data += received_data
        received_data = data_sock.recv(PACKET_SIZE)

    data_sock.close()

    with open(args, 'wb') as stor_file:
        stor_file.write(file_data)
        stor_file.close()

    return '226 Operation successful\r\n'

FTP_COMMANDS = {'OPTS': opts_command_handler, 
                'USER': user_command_handler,
                'PASS': pass_command_handler,
                'PORT': port_command_handler,
                'QUIT': quit_command_handler,
                'RETR': retr_command_handler,
                'STOR': stor_command_handler,
                }

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Starting up on {} port {}'.format(*FULL_ADDRS))

server_sock.bind(FULL_ADDRS)
server_sock.listen(1)

while True:
    print('Waiting for client...')

    cmd_sock, client_addr = server_sock.accept()

    print('Client connected from', client_addr)

    cmd_sock.send(client_connected_handler().encode())

    function_handler = None

    while function_handler != FTP_COMMANDS['QUIT']:
        
        message = (cmd_sock.recv(PACKET_SIZE)).decode()
        print('Received Message:', message.strip())
        (ftp_command, arguments) = command_parser(message)
        
        try:
            function_handler = FTP_COMMANDS[ftp_command]
        except KeyError:
            print("I don't know how to answer to this command!")
            response = '502 Command not implemented.\r\n'
        else:
            response = function_handler(arguments)
        
        cmd_sock.send(response.encode())

    print('Closing connection...')
    cmd_sock.close()
    print('Connection closed!')