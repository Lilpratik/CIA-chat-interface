import socket
import threading
from cryptography.fernet import Fernet
from hashlib import sha256

# Use the shared symmetric key (replace with the same key printed by the server)
key = b"xhdJqaxIKfxtE_bSH3linl4OO73stdhxeyMDDDS9Y2U="
f = Fernet(key)

delimiter = b"|||"

# Set up client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 8888
client_socket.connect((host, port))

def receive_messages():
    while True:
        try:
            # Receive message from server
            data = client_socket.recv(1024)
            if not data:
                break
            
            # Separate encrypted message and digest
            encrypted_message, received_digest = data.split(delimiter)
            
            # Decrypt message
            message = f.decrypt(encrypted_message).decode()
            
            # Check integrity
            digest = sha256(message.encode()).hexdigest()
            if digest == received_digest.decode():
                print(f"\nServer (Verified): {message}")
            else:
                print("Warning: Message integrity compromised!")
        except Exception as e:
            print(f"Error: {e}")
            break

# Start receiving messages in a separate thread
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Sending messages
while True:
    client_message = input("\nClient: ")
    encrypted_message = f.encrypt(client_message.encode())
    message_digest = sha256(client_message.encode()).hexdigest()
    client_socket.send(encrypted_message + delimiter + message_digest.encode())
