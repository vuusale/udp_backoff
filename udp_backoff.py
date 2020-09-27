import argparse
import socket
import datetime

MAX_BYTES = 65536
LOCALHOST = '127.0.0.1'
PORT = 9001

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.host, self.port))
        print(f"Server started on {sock.getsockname()}")

        while True:
            data, address = sock.recvfrom(MAX_BYTES)

            message = data.decode('ascii')
            print(f"The client {address} says: {message}")

            server_message = f"Hey! Your message was {len(data)} bytes long"
            server_data = server_message.encode('ascii')
            sock.sendto(server_data, address)


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.backoff = {1: 2, 2: 4, 3: 1}

    def interval(self):
        now = datetime.datetime.now().time()
        return 1 if datetime.time(12,0,0) < now < datetime.time(16,59,59) else (2 if datetime.time(17,0,0) < now < datetime.time(23,59,59) else 3)

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((self.host, self.port))
        print(f"Client socket name: {sock.getsockname()}")

        message = f"Hello server, the current date and time are {datetime.datetime.now().strftime('%b %d %Y %H:%M:%S')}"
        data = message.encode('ascii')

        delay = 0.1
        while True:
            sock.send(data)
            sock.settimeout(delay)

            try:
                data = sock.recv(MAX_BYTES)
                
            except socket.timeout as exc:
                interval = self.interval()
                delay *= 2 if interval % 2 else 3
                if delay > self.backoff[interval]:
                    raise RuntimeError("Something bad happened :(") from exc

            else:
                break

        message = data.decode('ascii')
        print(f"Server's message: {message}")
        


def main():
    choices = {"server", "client"}
    parser = argparse.ArgumentParser()
    parser.add_argument("choice", choices=choices, help="Type of connection")
    parser.add_argument("--host", "-H", metavar="HOST", type=str, help="Host address (default: localhost)", default=LOCALHOST)
    parser.add_argument("--port", "-P", metavar="PORT", type=int, help="Port number (default: 9001)", default=PORT)
    args = parser.parse_args()

    if args.choice == "client":
        client = Client(args.host, args.port)
        client.connect()
    elif args.choice == "server":
        server = Server(args.host, args.port)
        server.start()

if __name__ == "__main__":
    main()