import tkinter as tk
import socket
import threading
root = tk.Tk()
root.title("Chat")
root.geometry("600x300")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 5556)) 
chat_box = tk.Text(root, state="disabled", wrap="word")
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
def log_message(msg):
    chat_box.config(state="normal")
    chat_box.insert(tk.END, msg + "\n")
    chat_box.config(state="disabled")
    chat_box.see(tk.END)
def send_message(event=None):
    msg = entry1.get()  
    if msg.strip() != "":
        client_socket.sendall(msg.encode())
        log_message(f"You: {msg}")
        entry1.delete(0, tk.END)  
def receive_message():
    while True:
        reply = client_socket.recv(1024).decode()
        if not reply:
            break
        log_message(f"Server: {reply}")  
entry1 = tk.Entry(root, width=40)
entry1.pack(pady=10)
entry1.bind("<Return>", send_message)
button = tk.Button(root, text="Send", command=send_message)
button.pack(pady=10)
threading.Thread(target=receive_message, daemon=True).start()
root.mainloop()
client_socket.close()

