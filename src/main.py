import sys

from server.server import main as start_server
from client.client import main as start_client


def run_server():
    """
    Inicia o servidor responsável por intermediar a comunicação do chat.
    """
    start_server()


def run_client():
    """
    Inicia um cliente que se conecta ao servidor de chat.
    """
    start_client()


def main():
    """
    Define se o programa será executado como servidor ou cliente.
    """
    if len(sys.argv) != 2:
        print("Uso:")
        print("  python main.py server")
        print("  python main.py client")
        sys.exit(1)

    role = sys.argv[1].lower()

    if role == "server":
        run_server()
    elif role == "client":
        run_client()
    else:
        print("Opção inválida. Use 'server' ou 'client'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
