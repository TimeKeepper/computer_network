import socket

SERVER_ADDRESS = ('localhost', 8082)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind(SERVER_ADDRESS)
    print("Server is listening on", SERVER_ADDRESS[1])

    while True:
        message, client_address = server_socket.recvfrom(1024)
        print(f"Received message from {client_address}: {message.decode()}")
        server_socket.sendto(b"pong", client_address)
