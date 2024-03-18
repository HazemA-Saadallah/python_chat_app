import threading
import socket
import datetime
import tkinter
from tkinter import scrolledtext


class signal_handler:
    def __init__(self, run=True) -> None:
        """ self.window = tkinter.Tk() """
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

    def kill(self):
        self.run = False

class client:
    def __init__(self, address, port, name) -> None:
        self.name = name
        self.server_address = (address, port)
        self.signal_handler = signal_handler()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def gui_send(self):
        timestamp = datetime.datetime.now().strftime('%Y-%M-%d %H:%M:%S')
        massage = self.input_area.get('1.0', 'end')
        self.client_socket.send(f"[{timestamp}][{self.name}]: {self.input_area.get('1.0', 'end')}".encode())
        self.input_area.delete('1.0', 'end')

    def gui_recieve(self):
        while self.signal_handler.can_run():
            massage = self.client_socket.recv(1024).decode()
            timestamp = datetime.datetime.now().strftime('%Y-%M-%d %H:%M:%S')

            if massage == "__GET_NAME":
                self.client_socket.send(self.name.encode())
            elif massage == "__SUCCESSFUL_CONNECTION":
                self.text_area.config(state='normal')
                self.text_area.insert('end', f"[{timestamp}][INFO]: Successfully connected to server\n")
                self.text_area.config(state='disabled')

            elif massage == "__SERVER_KILL":
                self.text_area.config(state='normal')
                self.text_area.insert('end', f"[{timestamp}][Server]: Session terminated\n")
                self.text_area.config(state='disabled')
                break
            else:
                self.text_area.config(state='normal')
                self.text_area.insert('end', massage+"\n")
                self.text_area.config(state='disabled')

    def gui_exit(self):
        self.signal_handler.kill()
        self.client_socket.send("__CLIENT_EXIT".encode())
        self.client_socket.close()
        self.window.destroy()

    def start(self):
        self.gui_loop()
        self.client_socket.connect(self.server_address)
        receive_thread = threading.Thread(target=self.gui_recieve, daemon=True)
        receive_thread.start()
        self.window.mainloop()

    def gui_loop(self):
        self.window = tkinter.Tk()
        self.window.configure(bg="lightgray")

        self.chat_label = tkinter.Label(self.window, text="chat", bg="lightgray")
        self.chat_label.config(font=("Arial", 16))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = scrolledtext.ScrolledText(self.window)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disabled", font=("Arial", 16))

        self.msg_label = tkinter.Label(self.window, text="chat", bg="lightgray")
        self.msg_label.config(font=("Arial", 16))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.window, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.window, text="Send", command=self.gui_send)
        self.send_button.config(font=("Arial", 16))
        self.send_button.pack(padx=20, pady=5)

        self.exit_button = tkinter.Button(self.window, text="Exit", command=self.gui_exit)
        self.exit_button.config(font=("Arial", 16))
        self.exit_button.pack(padx=20, pady=5)

        self.window.protocol("WM_DELETE_WINDOW", self.gui_exit)


if __name__ == "__main__":
    client = client("localhost", 9999, input("Enter the name: "))
    client.start()
