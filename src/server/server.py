import threading
import socket

clients = {}


def handle_client(client):
    try:
        username = client.recv(2048).decode("utf-8")
        clients[client] = username
        print(f"{username} entrou no chat")
        broadcast_server(f">> {username} entrou no chat\n".encode("utf-8"))
    except Exception:
        client.close()
        return

    while True:
        try:
            msg = client.recv(2048)
            if not msg:
                break
            full_msg = f"{clients[client]}: {msg.decode('utf-8')}"
            broadcast_client(full_msg.encode("utf-8"), client)
        except Exception:
            break

    remove_client(client)


def broadcast_client(msg, sender):
    for client in list(clients.keys()):
        if client != sender:
            try:
                client.send(msg)
            except Exception:
                remove_client(client)


def broadcast_server(msg):
    for client in list(clients.keys()):
        try:
            client.send(msg)
        except Exception:
            remove_client(client)


def remove_client(client):
    if client in clients:
        username = clients[client]
        del clients[client]
        client.close()
        broadcast_server(f">> {username} saiu do chat\n".encode("utf-8"))
        print(f"{username} saiu")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 7777))
    server.listen()
    print("Servidor iniciado")

    while True:
        client, addr = server.accept()
        thread = threading.Thread(
            target=handle_client,
            args=(client,),
            daemon=True
        )
        thread.start()


if __name__ == "__main__":
    main()
