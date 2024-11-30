import tkinter as tk
from tkinter import simpledialog
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

class ChatClient:
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

        self.setup_client()

    def setup_client(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))
        self.log_message("Connected to the server")
        self.receive_thread = Thread(target=self.receive_messages)
        self.receive_thread.start()

    def send_message(self):
        message = self.message_entry.get()
        
        if message:
            encrypt_message = message.replace('a', '!').replace('b', '@').replace('c', '#').replace('d', '$').replace('e', '%').replace('f', '^').replace('g', '&').replace('h', '*').replace('i', '(').replace('j', ')').replace('k', '-').replace('l', '_').replace('m', '=').replace('n', '[').replace('o', ']').replace('p', '{').replace('q', '}').replace('r', ';').replace('s', ',').replace('t', '.').replace('u', '<').replace('v', '>').replace('w', '?').replace('x', '/').replace('y', '|').replace('z', '~')
            self.client_socket.send(encrypt_message.encode())
            self.log_message(f"Sent: {message}")
            self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            message = self.client_socket.recv(1024)
            if not message:
                break
            # Convert symbols back to original strings
            message = message.decode().replace('!', 'a').replace('@', 'b').replace('#', 'c').replace('$', 'd').replace('%', 'e').replace('^', 'f').replace('&', 'g').replace('*', 'h').replace('(', 'i').replace(')', 'j').replace('-', 'k').replace('_', 'l').replace('=', 'm').replace('[', 'n').replace(']', 'o').replace('{', 'p').replace('}', 'q').replace(';', 'r').replace(',', 's').replace('.', 't').replace('<', 'u').replace('>', 'v').replace('?', 'w').replace('/', 'x').replace('|', 'y').replace('~', 'z')
            self.log_message(f"Received: {message}")

    def log_message(self, message):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.see(tk.END)

def main():
    root = tk.Tk()
    
    # Ask the user for the IP address and port number
    host = simpledialog.askstring("IP Address", "Enter the IP Address:", parent=root)
    port = simpledialog.askinteger("Port", "Enter the Port Number:", parent=root)
    
    # If the user provides both host and port
    if host and port:
        app = ChatClient(root, host, port)
        root.mainloop()
    else:
        print("IP Address or Port was not provided. Exiting.")

if __name__ == "__main__":
    main()
