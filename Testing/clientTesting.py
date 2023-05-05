import socket
import sys

def client_main():
    # Double checks correct usage
    if(len(sys.argv) != 3):
        print("Usage: python client.py <server_(IP)_address> <server_port_number>")
        sys.exit()

    server_ip = socket.gethostbyname(sys.argv[1])
    print("Server IP: ", server_ip)
    
    port = int(sys.argv[2])
    print("Port: ", port)

    server_addr = (server_ip, port)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Get instance
    client_socket.connect(server_addr)  # Connect to the server

    message = input(" -> ")  # Take input from user

    # Finish if terminating character ;;;
    while message.lower().strip() != ';;;':
        # Default encoding is encoding="utf-8", errors="strict"
        client_socket.send(message.encode())  # Send message to server
        data = client_socket.recv(1024).decode()  # Receive response from server, maximum of 1024 bytes

        print("Received from server: " + str(data))  # Show message from server in terminal

        message = input(" -> ")  # Again take input before send loop restarts

    client_socket.close()  # Close the connection after terminating character


# Line to initiate and run the file
if __name__ == '__main__':
    client_main()