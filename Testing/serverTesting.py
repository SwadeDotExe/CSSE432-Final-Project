import socket
import sys

def server_main():
    # Double checks correct usage
    if(len(sys.argv) != 2):
       print("Usage: python server.py <port_number>")
       sys.exit()

    # Get the host name and IP and print them
    host = socket.gethostname()
    host_ip = socket.gethostbyname(host)
    print("Host Name: ", host)
    print("Host IP: ", host_ip)

    # Get the port to host the server on
    port = int(sys.argv[1])
    print("Port: ", port)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Get instance
    # The bind() function takes a tuple as argument
    # The blank string allows other computers to connect
    server_socket.bind(('', port))  # Bind host address and port together

    # Configure how many clients the server can listen simultaneously...
    server_socket.listen(2)
    while True: # Keep looping for new clients when previous close
        (client_conn, client_address) = server_socket.accept()  # Accept new connection
        print("Connection from client: " + str(client_address) + ".")
        while True:
            # Receive data stream. Won't accept data packet greater than 1024 bytes...
            data = client_conn.recv(1024).decode()
            if not data:
                # If data is not received, connection is broken so break
                break
            print("From connected user: " + str(data))
            # data = input(' -> ')
            data = str(data).upper()
            client_conn.send(data.encode())  # Send data back to the client

        print("Connected client disconnected.")
        client_conn.close()  # Close the connection if client stops sending data
    
    server_socket.close() # Close the server at the end when terminating


# Line to initiate and run the file
if __name__ == '__main__':
    server_main()