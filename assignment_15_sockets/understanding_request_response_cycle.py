import socket

# Create socket
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to socket
my_socket.connect(('data.pr4e.org', 80))

# Create GET request
command = 'GET http://data.pr4e.org/intro-short.txt HTTP/1.0\r\n\r\n'.encode()
# Send a GET request
my_socket.send(command)

while True:
    # Receive data
    data = my_socket.recv(512)
    if (len(data) < 1):
        break
    print(data.decode())

# Close socket
my_socket.close()