import threading
import socket

clients = {}
available_ids = {1, 2}
clients_lock = threading.Lock()


def handle_client(client):
    try:
        username = client.recv(2048).decode("utf-8")

        with clients_lock:
            if not available_ids:
                client.send(
                    "Servidor cheio (máx 2 usuários)\n".encode("utf-8")
                )
                client.close()
                return

            user_id = min(available_ids)
            available_ids.remove(user_id)
            clients[client] = {"id": user_id, "name": username}

        print(f"{username} entrou")
        broadcast_server(
            f">> {username} entrou no chat\n".encode("utf-8")
        )

    except Exception:
        client.close()
        return

    while True:
        try:
            msg = client.recv(2048)
            if not msg:
                break

            with clients_lock:
                if client not in clients:
                    break
                user = clients[client]

            full_msg = f"{user['name']}: {msg.decode('utf-8')}"
            broadcast_client(full_msg.encode("utf-8"), client)

        except Exception:
            print("\nOcorreu um erro inesperado")
            break

    remove_client(client)


def broadcast_client(msg, sender):
    with clients_lock:
        targets = list(clients.keys())

    for client in targets:
        if client != sender:
            try:
                client.send(msg)
            except Exception:
                print("\nOcorreu um erro inesperado")
                remove_client(client)


def broadcast_server(msg):
    with clients_lock:
        targets = list(clients.keys())

    for client in targets:
        try:
            client.send(msg)
        except Exception:
            print("\nOcorreu um erro inesperado")
            remove_client(client)


def remove_client(client):
    with clients_lock:
        if client not in clients:
            return

        user = clients[client]
        del clients[client]
        available_ids.add(user["id"])

    client.close()
    broadcast_server(
        f">> {user['name']} saiu do chat\n".encode("utf-8")
    )
    print(f"{user['name']} saiu")


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
