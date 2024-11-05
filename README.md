# Python Secure Chat Application with CIA Verification

A Python-based chat application that demonstrates client-server communication with cryptographic support to maintain **Confidentiality**, **Integrity**, and **Availability** (CIA) of messages. This application uses the `cryptography` library for secure message encryption and hashing to ensure message integrity, making it ideal for learning secure communication principles in networked applications.

## Features
- **Confidentiality**: Messages are encrypted using the `Fernet` symmetric encryption provided by the `cryptography` library.
- **Integrity**: Each message is hashed with `SHA-256` to ensure the message content hasn’t been altered.
- **Availability**: A server capable of handling multiple clients concurrently through threading, making it available to respond to multiple users.

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/python-secure-chat-app.git
