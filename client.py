import socket


client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)

client.connect(
    ("127.0.0.1", 1234)
)

while True:
    data= client.recv(2048) #receive
    print(data.decode())