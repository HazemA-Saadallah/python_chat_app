import threading
import socket
import datetime


class signal_handler:
    def __init__(self, run=True) -> None:
        self.run = run
        self.commands = {
            "get_client_name": "__GET_NAME",
            "client_successful_connection": "__SUCCESSFUL_CONNECTION",
            "/exit": "__CLIENT_EXIT"
        }

    def command(self, operation):
        return self.commands[operation]

    def order(self, operation, client_name):
        if (operation == "__GET_NAME"):
            return client_name

    def can_run(self):
        return self.run


class client:
    def __init__(self, address, port, name) -> None:
        self.name = name
        self.server_address = (address, port)
        self.signal_handler = signal_handler()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive(self):
        while self.signal_handler.can_run():
            massage = self.client_socket.recv(1024).decode()
            timestamp = datetime.datetime.now().strftime('%Y-%M-%d %H:%M:%S')

            if massage == "__GET_NAME":
                self.client_socket.send(self.name.encode())
            elif massage == "__SUCCESSFUL_CONNECTION":
                print(f"[{timestamp}][INFO]: Successfully connected to server")
            elif massage == "__SERVER_KILL":
                print(f"[{timestamp}][Server]: Session terminated")
                break
            else:
                print(massage)

    def send(self):
        while self.signal_handler.can_run():
            timestamp = datetime.datetime.now().strftime('%Y-%M-%d %H:%M:%S')
            enterd_massage = input('')

            if enterd_massage == '/exit':
                self.client_socket.send(self.signal_handler.command(enterd_massage).encode())
                self.client_socket.close()
                break
            elif enterd_massage.strip() != "":
                self.client_socket.send(f"[{timestamp}][{self.name}]: {enterd_massage}".encode())

    def start(self):
        self.client_socket.connect(self.server_address)
        receive_thread = threading.Thread(target=self.receive, daemon=True)
        receive_thread.start()

        send_thread = threading.Thread(target=self.send)
        send_thread.start()


if __name__ == "__main__":
    client = client("localhost", 9999, input("Enter the name: "))
    client.start()
