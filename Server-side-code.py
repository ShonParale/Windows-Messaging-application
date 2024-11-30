import tkinter as tk
from tkinter import simpledialog
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

# Define the message encryption and decryption dictionaries
encrypt_dict = {'a': '!', 'b': '@', 'c': '#', 'd': '$', 'e': '%', 'f': '^', 'g': '&', 'h': '*', 'i': '(', 'j': ')',
                'k': '-', 'l': '_', 'm': '=', 'n': '[', 'o': ']', 'p': '{', 'q': '}', 'r': ';', 's': ',', 't': '.',
                'u': '<', 'v': '>', 'w': '?', 'x': '/', 'y': '|', 'z': '~'}
decrypt_dict = {v: k for k, v in encrypt_dict.items()}


class ChatApp:
    def __init__(self, master, host, port):
        self.master = master
        self.master.title("Chat Application")
        self.chat_log = tk.Text(master, state=tk.DISABLED)
        self.chat_log.pack(pady=10)
        self.message_entry = tk.Entry(master)
        self.message_entry.pack(pady=10)
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)

        self.server_host = host
        self.server_port = port

        self.setup_server()

    def setup_server(self):
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((self.server_host, self.server_port))
        self.server_socket.listen(5)
        self.log_message("Sent: Server started. Waiting for connections...")
        self.client_socket, client_address = self.server_socket.accept()
        self.log_message(f"Received: Connected to {client_address}")
        self.receive_thread = Thread(target=self.receive_messages)
        self.receive_thread.start()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            # Convert the message to symbols
            encrypted_message = ''.join(encrypt_dict.get(c, c) for c in message)
            self.client_socket.send(encrypted_message.encode())
            self.log_message(f"Sent: {message}")
            self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            message = self.client_socket.recv(1024)
            if not message:
                break
            # Convert the received data from symbols to original string
            decrypt_message = ''.join(decrypt_dict.get(c, c) for c in message.decode())
            self.log_message(f"Received: {decrypt_message}")

    def log_message(self, message):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.see(tk.END)


def main():
    root = tk.Tk()

    # Ask the user for the IP address and port number
    host = simpledialog.askstring("IP Address", "Enter the IP Address to bind the server:", parent=root)
    port = simpledialog.askinteger("Port", "Enter the Port Number to bind the server:", parent=root)

    # If the user provides both host and port
    if host and port:
        app = ChatApp(root, host, port)
        root.mainloop()
    else:
        print("IP Address or Port was not provided. Exiting.")


if __name__ == "__main__":
    main()
