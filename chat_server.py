import socket
import threading
from cryptography.fernet import Fernet
from hashlib import sha256

# Define shared symmetric key (should be the same for both client and server)
#key = Fernet.generate_key()  # In production, securely share this key
key = b"xhdJqaxIKfxtE_bSH3linl4OO73stdhxeyMDDDS9Y2U="
print("Generated Key (Keep this safe and use the same on the client):", key.decode())
f = Fernet(key)

delimiter = b"|||"
confidentiality = False
integrity = False
authentication = False

# Set up server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 8888
server_socket.bind((host, port))
server_socket.listen(5)
print(f"Server started on {host}:{port}")

def handle_client(client_socket, address):
    global confidentiality, integrity, authentication
    print(f"Connection from {address}")

    while True:
        try:
            # Receive message
            data = client_socket.recv(1024)
            if not data:
                break

            # Separate encrypted message and digest
            encrypted_message, received_digest = data.split(delimiter)
            
            # Decrypt the message
            message = f.decrypt(encrypted_message).decode()
            confidentiality = True
            
            # Generate digest to verify integrity
            digest = sha256(message.encode()).hexdigest()
            if digest == received_digest.decode():
                integrity = True
            authentication = True

            print(f"Client: {message}")
            
            # CIA verification
            if confidentiality and integrity and authentication:
                print("CIA verified")
            else:
                print("CIA not verified")

            # Server reply
            server_message = input("Server: ")
            encrypted_response = f.encrypt(server_message.encode())
            response_digest = sha256(server_message.encode()).hexdigest()
            client_socket.send(encrypted_response + delimiter + response_digest.encode())
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

while True:
    client_socket, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()
