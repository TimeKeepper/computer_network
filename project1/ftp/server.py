import socket
import os

# 服务器的IP地址和端口
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

def handle_client(client_socket):
    try:
        file_name = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Client requested file: {file_name}")

        if os.path.exists(file_name):
            client_socket.send(b"OK")
            
            with open(file_name, 'rb') as file:
                while True:
                    file_data = file.read(BUFFER_SIZE)
                    if not file_data:
                        break
                    client_socket.send(file_data)
            print(f"File {file_name} sent successfully.")
        else:
            client_socket.send(b"File not found")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        handle_client(client_socket)

