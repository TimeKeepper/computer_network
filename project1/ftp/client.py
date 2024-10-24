import socket

SERVER_HOST = 'localhost'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    file_name = input("Enter the file name you want to request: ")
    
    client_socket.send(file_name.encode())

    response = client_socket.recv(BUFFER_SIZE).decode()
    
    if response == "OK":
        with open(f"received_file", 'wb') as file:
            while True:
                file_data = client_socket.recv(BUFFER_SIZE)
                if not file_data:
                    break
                file.write(file_data)
        print(f"File {file_name} received successfully.")
    else:
        print(f"Error: {response}")

