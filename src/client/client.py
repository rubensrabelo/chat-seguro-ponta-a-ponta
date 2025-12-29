import threading
import socket


def receiveMessages(client):
    while True:
        try:
            msg = client.recv(2048).decode("utf-8")
            print(msg+"\n")
        except Exception as e:
            print(f"\nErro {e}\n")
            print("Pressione <Enter> Para continuar...")
            client.close()
            break


def sendMessages(client, username):
    while True:
        try:
            msg = input("\n")
            client.send(f"<{username}> {msg}".encode("utf-8"))
        except Exception as e:
            print(f"\nErro {e}\n")
            return


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(("localhost", 7777))
    except Exception as e:
        return print(f"\nErro: {e}\n")

    username = input("Usuário> ")
    print("\nConectado")

    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])

    thread1.start()
    thread2.start()


if __name__ == "__main__":
    main()
