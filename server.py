import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 5555))
server.listen()

clients = []

print("Server started...")

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            print("Message received:", message.decode())  # 👈 SERVER LOG
            broadcast(message, client)
        except:
            clients.remove(client)
            client.close()
            print("Client disconnected")
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")
        clients.append(client)

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()
