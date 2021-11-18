
from Socket import Socket
from threading import Thread

class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()

    def set_up(self):
        self.connect(
            ("127.0.0.1",1234)
        )
        send_thread =Thread(target=self.send_data, args=(None,))
        send_thread.start()

    def listen_socket(self, listened_socket=None):
        while True:
        data = self.recv(2048)  # receive
        print(data.decode())

    def send_data(self,data):
        while True:
            self.send(input(":::").encode("utf-8"))

if __name__ == '__main__':
    send_server()