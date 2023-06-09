import cv2
import socket
import struct
import pickle

# Server IP and port
SERVER_IP = '192.168.68.105'
SERVER_PORT = 9999

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Receive and display frames
while True:
    # Receive message from server
    message = b''
    while len(message) < struct.calcsize("Q"):
        chunk = client_socket.recv(4 * 1024)  # 4KB chunk size
        if not chunk:
            break
        message += chunk

    # Unpack frame size and data
    packed_msg_size = message[:struct.calcsize("Q")]
    message = message[struct.calcsize("Q"):]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    # Reconstruct frame
    while len(message) < msg_size:
        message += client_socket.recv(4 * 1024)  # 4KB chunk size

    frame_data = message[:msg_size]
    message = message[msg_size:]
    frame = pickle.loads(frame_data)

    # Display frame
    cv2.imshow('Live Camera', frame)
    cv2.waitKey(1)

# Close connection
client_socket.close()
cv2.destroyAllWindows()
