import threading
import socket

clients = []


def handle_client(client):
    while True:
        try:
            msg = client.recv(2048)
            broadcast(msg, client)
        except Exception as e:
            print(f"\nErro: {e}\n")
            remove_client(client)
            break


def broadcast(msg, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(msg)
            except Exception as e:
                print(f"\nErro: {e}\n")
                remove_client(client)


def remove_client(client):
    clients.remove(client)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Iniciou o servidor de bate-papo")

    try:
        server.bind(("localhost", 7777))
        server.listen()
    except Exception as e:
        return print(f"\nErro: {e}\n")

    while True:
        client, addr = server.accept()
        clients.append(client)
        print(f"Cliente conectado com sucesso. IP: {addr}")

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    main()
