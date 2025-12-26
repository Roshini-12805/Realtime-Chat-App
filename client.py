import socket
import threading
import tkinter as tk
from tkinter import simpledialog

# Socket setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5555))

# Tkinter window
window = tk.Tk()
window.title("Realtime Chat")
window.geometry("400x500")
window.configure(bg="#ECE5DD")

# Username
username = simpledialog.askstring("Username", "Enter your name", parent=window)

# Chat area
chat_area = tk.Text(window, bg="white", state='disabled', wrap='word')
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Configure tags
chat_area.tag_configure("left", justify="left")
chat_area.tag_configure("right", justify="right")

# Message entry
message_entry = tk.Entry(window)
message_entry.pack(padx=10, pady=5, fill=tk.X)

def show_message(message, tag):
    chat_area.config(state='normal')
    chat_area.insert(tk.END, message + "\n", tag)
    chat_area.config(state='disabled')
    chat_area.see(tk.END)

def send_message():
    message = message_entry.get()
    if message:
        # Show sender message on RIGHT
        show_message("You: " + message, "right")
        client.send(f"{username}: {message}".encode())
        message_entry.delete(0, tk.END)

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            # Show receiver message on LEFT
            show_message(message, "left")
        except:
            break

send_button = tk.Button(
    window, text="Send", command=send_message,
    bg="#25D366", fg="white"
)
send_button.pack(pady=5)

# Background thread
thread = threading.Thread(target=receive_messages)
thread.daemon = True
thread.start()

window.mainloop()
client.close()
