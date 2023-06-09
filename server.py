import cv2
import socket
import struct
import pickle
import threading

# Server IP and port
SERVER_IP = '192.168.68.105'
SERVER_PORT = 9999

# Function to handle client connections
def handle_client(client_socket, client_address):
    print(f'[*] New connection from {client_address}')

    # Open camera
    cap = cv2.VideoCapture(0)

    while True:
        # Read frame from camera
        ret, frame = cap.read()

        # Serialize frame
        data = pickle.dumps(frame)

        # Pack frame size and data
        message = struct.pack("Q", len(data)) + data

        try:
            # Send frame to client
            client_socket.sendall(message)
        except:
            # If client connection is lost, break the loop
            break

    # Release camera and close connection
    cap.release()
    client_socket.close()
    print(f'[*] Connection closed from {client_address}')


def start_server():
    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket to IP and port
    server_socket.bind((SERVER_IP, SERVER_PORT))

    # Listen for connections
    server_socket.listen(2)
    print('[*] Server started')

    while True:
        # Accept client connections
        client_socket, client_address = server_socket.accept()

        # Handle client in a separate thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


# Start the server
start_server()
