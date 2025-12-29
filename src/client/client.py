import sys
import threading
import socket

stop_event = threading.Event()


def receiveMessages(client):
    while not stop_event.is_set():
        try:
            msg = client.recv(2048)
            if not msg:
                print("Conexão encerrada pelo servidor")
                print("Pressione Enter para sair...")
                stop_event.set()
                client.close()
                break
            print(msg.decode("utf-8"))
        except Exception:
            print("\nErro de conexão.")
            print("Pressione Enter para sair...")
            stop_event.set()
            client.close()
            break


def sendMessages(client):
    while not stop_event.is_set():
        try:
            msg = input()
            if stop_event.is_set():
                break
            client.send(msg.encode("utf-8"))
        except Exception:
            stop_event.set()
            client.close()
            break


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 7777))

    username = input("Usuário> ")
    client.send(username.encode("utf-8"))

    print(">> Conectado ao chat\n")

    t1 = threading.Thread(target=receiveMessages, args=(client,))
    t2 = threading.Thread(target=sendMessages, args=(client,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    sys.exit(0)


if __name__ == "__main__":
    main()
