import threading
import socket


def receiveMessages(client):
    while True:
        try:
            msg = client.recv(2048).decode("utf-8")
            if not msg:
                break
            print(msg)
        except Exception:
            break


def sendMessages(client):
    while True:
        try:
            msg = input()
            client.send(msg.encode("utf-8"))
        except Exception:
            break


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 7777))

    username = input("Usuário> ")
    client.send(username.encode("utf-8"))

    print(">> Conectado ao chat\n")

    threading.Thread(
        target=receiveMessages,
        args=(client,),
        daemon=True
    ).start()
    threading.Thread(
        target=sendMessages,
        args=(client,),
        daemon=True
    ).start()

    while True:
        pass


if __name__ == "__main__":
    main()
