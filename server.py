import socket 
import threading
import time
from datetime import datetime

connections = []
messages_queue = []
last_broadcast_time = time.time()
BROADCAST_INTERVAL = 10
MULTICAST_GROUP = '233.0.0.1'
MULTICAST_PORT = 1502

def broadcast_messages():
    global messages_queue, last_broadcast_time
    
    while True:
        time.sleep(1)
        current_time = time.time()
        
        if (current_time - last_broadcast_time >= BROADCAST_INTERVAL and 
            messages_queue):
            
            messages_packet = ""
            for msg in messages_queue:
                messages_packet += f"{msg}\n"
            
            try:
                udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
                
                udp_socket.sendto(
                    messages_packet.encode('utf-8'), 
                    (MULTICAST_GROUP, MULTICAST_PORT)
                )
                udp_socket.close()
                
                print(f"Отправлена порция из {len(messages_queue)} сообщений через multicast")
                
                messages_queue.clear()
                
            except Exception as e:
                print(f'Error broadcasting via multicast: {e}')
            
            last_broadcast_time = current_time

def handle_user_connection(connection: socket.socket, address: str) -> None:
    while True:
        try:
            msg = connection.recv(1024)

            if msg:
                message_text = msg.decode()
                print(f'{address[0]}:{address[1]} - {message_text}')
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                formatted_message = f'[{timestamp}] {address[0]}:{address[1]} - {message_text}'
                messages_queue.append(formatted_message)

            else:
                remove_connection(connection)
                break

        except Exception as e:
            print(f'Error to handle user connection: {e}')
            remove_connection(connection)
            break

def remove_connection(conn: socket.socket) -> None:
    if conn in connections:
        conn.close()
        connections.remove(conn)

def server() -> None:
    LISTENING_PORT = 12000
    
    try:
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('127.0.0.1', LISTENING_PORT))
        socket_instance.listen(4)

        print('Server running!')
        
        broadcast_thread = threading.Thread(target=broadcast_messages)
        broadcast_thread.daemon = True
        broadcast_thread.start()
        
        while True:
            socket_connection, address = socket_instance.accept()
            if socket_connection:
                connections.append(socket_connection)
                print(f"{address} connected")
            threading.Thread(target=handle_user_connection, args=[socket_connection, address]).start()

    except Exception as e:
        print(f'An error has occurred when instancing socket: {e}')
    finally:
        if len(connections) > 0:
            for conn in connections:
                remove_connection(conn)
        socket_instance.close()

if __name__ == "__main__":
    server()