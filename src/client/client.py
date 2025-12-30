import sys
import threading
import socket
import os

from crypto import rsa_utils, cbc, ctr

stop_event = threading.Event()

# ESTADO CRIPTOGRÁFICO
private_key, public_key = rsa_utils.generate_keys()
session_key = None
mode = None

MODE_FILE = "./src/client/crypto_mode.txt"


def save_mode(selected_mode):
    with open(MODE_FILE, "w") as f:
        f.write(selected_mode)


def load_mode():
    if not os.path.exists(MODE_FILE):
        return None
    with open(MODE_FILE, "r") as f:
        return f.read().strip()


def receiveMessages(client):
    global session_key

    while not stop_event.is_set():
        try:
            msg = client.recv(4096)
            if not msg:
                break

            # TROCA DE CHAVES
            if msg.startswith(b"RSAKEY:"):
                other_pub = msg[7:]
                if user_id == 1:
                    session_key = os.urandom(16)
                    encrypted = rsa_utils.encrypt_with_public_key(
                        other_pub, session_key
                    )
                    client.send(b"SESSION:" + encrypted)

            elif msg.startswith(b"SESSION:"):
                encrypted = msg[8:]
                session_key = rsa_utils.decrypt_with_private_key(
                    private_key, encrypted
                )
                print(">> Chave de sessão estabelecida")

            else:
                if session_key:
                    data = msg
                    plaintext = (
                        cbc.decrypt(session_key, data)
                        if mode == "CBC"
                        else ctr.decrypt(session_key, data)
                    )
                    print(plaintext.decode(errors="ignore"))
                else:
                    print(msg.decode(errors="ignore"))

        except Exception:
            stop_event.set()
            break


def sendMessages(client):
    while not stop_event.is_set():
        msg = input()
        if session_key:
            data = (
                cbc.encrypt(session_key, msg.encode())
                if mode == "CBC"
                else ctr.encrypt(session_key, msg.encode())
            )
            client.send(data)
        else:
            client.send(msg.encode())


def main():
    global user_id, mode

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 7777))

    username = input("Usuário> ")
    client.send(username.encode())

    # RECEBE ID
    user_id = int(client.recv(16).decode().split(":")[1])
    print(f">> Seu ID: {user_id}")

    if user_id == 1:
        mode = input("Modo (CBC/CTR)> ").strip().upper()
        save_mode(mode)  # <<< SALVA O MODO
    else:
        mode = load_mode()  # <<< CARREGA O MODO
        print(f">> Modo carregado: {mode}")

    # ENVIA CHAVE PÚBLICA
    client.send(b"RSAKEY:" + public_key)

    t1 = threading.Thread(target=receiveMessages, args=(client,))
    t2 = threading.Thread(target=sendMessages, args=(client,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    sys.exit(0)


if __name__ == "__main__":
    main()
