import tkinter as tk
import webbrowser
import socket
import threading
import google.generativeai as genai
genai.configure(api_key="AIzaSyA7pGp-7gaptTNPsB-yd-yirIV0IxZ6Z7U")
model = genai.GenerativeModel("gemini-1.5-flash")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
root = tk.Tk()
root.title("Chat")
root.geometry("600x400")
chat_box = tk.Text(root, state="disabled", wrap="word")
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
def log_message(msg):
    chat_box.config(state="normal")
    chat_box.insert(tk.END, msg + "\n")
    chat_box.config(state="disabled")
    chat_box.see(tk.END)
server_socket.bind(("127.0.0.1", 5556))
server_socket.listen(1)
log_message("Server is running... Waiting for client connection.")
conn, addr = server_socket.accept()
log_message(f"Connected by {addr}")
def Receivemessage():
    while True:
        data = conn.recv(1024).decode().strip()
        if data == "STOP":
            log_message("Connection closed.")
            break
        if data == "open youtube":
            webbrowser.open("https://youtube.com")
            log_message("Opening YouTube")
        elif data == "open spotify":
            webbrowser.open("https://spotify.com")
            log_message("Opening Spotify")
        elif data == "open instagram":
            webbrowser.open("https://instagram.com")
            log_message("Opening Instagram")
        elif data.startswith("open "):
            site_name = data.replace("open ", "").strip()
            url = f"https://{site_name}.com"
            webbrowser.open(url)
            log_message(f"Trying to open {site_name} at {url}")
        log_message(f"Client: {data}")
        response = model.generate_content(data)
        reply = response.text if response and response.text else "No response."
        conn.sendall(reply.encode())
        log_message(f"AI: {reply}")
def Sendmessage(event=None):
    data = entry1.get()
    if data.strip():
        conn.sendall(data.encode())
        log_message(f"You: {data}")
        entry1.delete(0, tk.END)
entry1 = tk.Entry(root)
entry1.pack(fill=tk.X, padx=10, pady=5)
button = tk.Button(root, text="Send", command=Sendmessage)
button.pack()
entry1.bind("<Return>", Sendmessage)
threading.Thread(target=Receivemessage, daemon=True).start()
root.mainloop()
conn.close()
server_socket.close()

