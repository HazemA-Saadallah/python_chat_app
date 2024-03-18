import threading
import socket
import datetime


class signal_handler:
    def __init__(self, run=True) -> None:
        self.run = run
        self.commands = {
            "get_client_name": "__GET_NAME",
            "client_successful_connection": "__SUCCESSFUL_CONNECTION"
        }

    def command(self, operation):
        return self.commands[operation]

    def can_run(self):
        return self.run

    def kill(self):
        self.run = False


class server:
    def __init__(self, address, port, state=False) -> None:
        self.clinets_list = []
        self.threads_list = []
        self.state = state
        self.server_address = (address, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(self.server_address)
        self.server_socket.listen()
        self.signal_handler = signal_handler()

    def receive_connection(self):
        while self.signal_handler.can_run():
            try:
                client_obj, client_address = self.server_socket.accept()
            except KeyboardInterrupt:
                self.broadcast("__SERVER_KILL")
                for client in self.clinets_list:
                    client.close()
                self.signal_handler.kill()

            client_obj.send(self.signal_handler.command("get_client_name").encode())
            clinet_name = client_obj.recv(1024).decode()
            self.clinets_list.append(client_obj)

            timestamp = datetime.datetime.now().strftime('%Y-%M-%d %H:%M:%S')

            print(f"[{timestamp}]: {clinet_name} connected\nAddress: ({str(client_address[0])}, {str(client_address[1])})")
            client_obj.send(self.signal_handler.command("client_successful_connection").encode())
            self.broadcast(f"[{timestamp}][Server]: {clinet_name} has joined the chat")

            self.threads_list.append(threading.Thread(target=self.handle_client, args=(client_obj, clinet_name), daemon=True))
            if self.state:
                self.threads_list[-1].start()

    def handle_client(self, client, name):
        while self.signal_handler.can_run():
            massage = client.recv(1024).decode()
            if (massage == "__CLIENT_EXIT"):
                timestamp = datetime.datetime.now().strftime('%Y-%M-%d %H:%M:%S')
                client.close()
                self.clinets_list.remove(client)
                self.broadcast(f"[{timestamp}][Server]: {name} has left the chat")
                break
            else:
                self.broadcast(massage)

    def broadcast(self, massage):
        for client in self.clinets_list:
            client.send(massage.encode())

    def start(self):
        self.state = True
        for thread in self.threads_list:
            if (not thread.is_alive()):
                thread.start()
        self.receive_connection()


if __name__ == "__main__":
    server_obj = server("localhost", 9999, True)
    server_obj.start()
