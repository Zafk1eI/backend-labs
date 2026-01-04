import socket
import threading

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 12000
MULTICAST_GROUP = '233.0.0.1'
MULTICAST_PORT = 1502

def handle_multicast_messages():
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_socket.bind(('', MULTICAST_PORT))
        
        group = socket.inet_aton(MULTICAST_GROUP)
        mreq = group + socket.inet_aton('0.0.0.0')
        udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
        while True:
            data, _ = udp_socket.recvfrom(4096)
            print(data.decode('utf-8'))
                
    except Exception as e:
        print(f'Error handling multicast messages: {e}')

    try:
        multicast_thread = threading.Thread(target=handle_multicast_messages)
        multicast_thread.daemon = True
        multicast_thread.start()

        print('Connected to chat! Send messages (type "quit" to exit)')

        while True:
            msg = input()

            if msg == 'quit':
                break

            socket_instance = socket.socket()
            socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
            socket_instance.send(msg.encode())
            socket_instance.close()

    except Exception as e:
        print(f'Error connecting to server socket {e}')

def client() -> None:

    SERVER_ADDRESS = '127.0.0.1'
    SERVER_PORT = 12000

    try:
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        multicast_thread = threading.Thread(target=handle_multicast_messages)
        multicast_thread.daemon = True
        multicast_thread.start()

        print('Connected to chat!')

        while True:
            msg = input()

            if msg == 'quit':
                break

            socket_instance.send(msg.encode())

        socket_instance.close()

    except Exception as e:
        print(f'Error connecting to server socket {e}')
    finally:
        socket_instance.close()


if __name__ == "__main__":
    client()