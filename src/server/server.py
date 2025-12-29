import threading
import socket

clients = {}


def handle_client(client):
    try:
        username = client.recv(2048).decode("utf-8")
        clients[client] = username
        print(f"{username} entrou no chat")
        broadcast(f">> {username} entrou no chat\n".encode("utf-8"), client)
    except Exception as e:
        print(f"\nErro: {e}\n")
        client.close()
        return

    while True:
        try:
            msg = client.recv(2048)
            if not msg:
                break
            full_msg = f"{clients[client]}: {msg.decode('utf-8')}"
            broadcast(full_msg.encode("utf-8"), client)
        except Exception as e:
            print(f"\nErro: {e}\n")
            break

    remove_client(client)


def broadcast(msg, sender):
    for client in list(clients.keys()):
        if sender is not None or client != sender:
            try:
                client.send(msg)
            except Exception as e:
                print(f"\nErro: {e}\n")
                remove_client(client)


def remove_client(client):
    if client in clients:
        username = clients[client]
        del clients[client]
        client.close()
        broadcast(f">> {username} saiu do chat\n".encode("utf-8"), None)
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
