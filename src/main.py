import sys

# IMPORTA as funções main já existentes
from server.server import main as start_server
from client.client import main as start_client


def run_server():
    """
    Função responsável por iniciar o servidor de chat.
    Deve ser executada em um terminal separado.
    """
    start_server()


def run_client():
    """
    Função responsável por iniciar um cliente do chat.
    Cada cliente deve ser executado em um terminal separado.
    """
    start_client()


def main():
    """
    Ponto de entrada principal do sistema.
    Permite escolher se o processo será servidor ou cliente.
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
