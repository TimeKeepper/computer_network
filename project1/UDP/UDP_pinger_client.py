import socket
import time

SERVER_ADDRESS = ('localhost', 8082)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    client_socket.settimeout(1)

    for i in range(4):
        message = b'ping'
        start_time = time.time()

        client_socket.sendto(message, SERVER_ADDRESS)
        print(f"Sent {message} to {SERVER_ADDRESS}")

        try:
            response, _ = client_socket.recvfrom(1024)
            end_time = time.time()
            rtt = (end_time - start_time) * 1000
            print(f"Received {response} from {SERVER_ADDRESS} in {rtt:.2f} ms")
        except socket.timeout:  
            print(f"Request timed out")


