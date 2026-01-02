import threading
import socket

clients = {}
available_ids = {1, 2}
clients_lock = threading.Lock()


def handle_client(client):
    """
    Gerencia a conexão e repassa mensagens de um cliente.
    """
    try:
        username = client.recv(2048).decode("utf-8")

        with clients_lock:
            if not available_ids:
                client.send(
                    b"Servidor cheio (max 2 usuarios)\n"
                )
                client.close()
                return

            user_id = min(available_ids)
            available_ids.remove(user_id)
            clients[client] = {"id": user_id, "name": username}

        client.send(f"ID:{user_id}".encode("utf-8"))

        print(f"{username} entrou (ID {user_id})")
        broadcast_server(
            f">> {username} entrou no chat\n".encode("utf-8")
        )

    except Exception:
        client.close()
        return

    while True:
        try:
            msg = client.recv(4096)
            if not msg:
                break

            with clients_lock:
                if client not in clients:
                    break

            broadcast_client(msg, client)

        except Exception:
            break

    remove_client(client)


def broadcast_client(msg, sender):
    """
    Envia mensagem de um cliente para os demais conectados.
    """
    with clients_lock:
        targets = list(clients.keys())

    for client in targets:
        if client != sender:
            try:
                client.send(msg)
            except Exception:
                remove_client(client)


def broadcast_server(msg):
    """
    Envia mensagens do servidor para todos os clientes.
    """
    with clients_lock:
        targets = list(clients.keys())

    for client in targets:
        try:
            client.send(msg)
        except Exception:
            remove_client(client)


def remove_client(client):
    """
    Remove um cliente e libera seu ID.
    """
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
    """
    Inicia o servidor e aceita conexões de clientes.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 7777))
    server.listen()
    print("Servidor iniciado")

    while True:
        client, _ = server.accept()
        threading.Thread(
            target=handle_client,
            args=(client,),
            daemon=True
        ).start()


if __name__ == "__main__":
    main()
