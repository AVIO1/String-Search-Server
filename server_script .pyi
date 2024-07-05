import socket
import threading
import time
import ssl
import configparser
from typing import Optional

class StringSearchServer:
    def __init__(self, config_file_path: str, reread_on_query: bool, port: int, use_ssl: bool):
        self.config_file_path = config_file_path
        self.reread_on_query = reread_on_query
        self.port = port
        self.use_ssl = use_ssl
        self.load_config()
        self.load_data()

    def load_config(self) -> None:
        """
        Load configuration settings from the specified config file.
        """
        config = configparser.ConfigParser()
        config.read(self.config_file_path)
        if 'DEFAULT' in config and 'linuxpath' in config['DEFAULT']:
            self.file_path = config['DEFAULT']['linuxpath']
        else:
            raise ValueError("Configuration file does not contain 'linuxpath' setting.")

    def load_data(self) -> None:
        """
        Load data from the specified file path.
        """
        with open(self.file_path, 'r') as file:
            self.data = file.read().splitlines()

    def run(self) -> None:
        """
        Start the server and handle client connections.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.use_ssl:
            self.server_socket = ssl.wrap_socket(self.server_socket, server_side=True, certfile='server.crt', keyfile='server.key')

        self.server_socket.bind(('135.181.96.160', self.port))  # Bind to all interfaces
        self.server_socket.listen(5)
        while True:
            client_socket, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()

    def handle_client(self, client_socket: socket.socket, addr: tuple) -> None:
        """
        Handle client requests.
        """
        start_time = time.time()
        query = client_socket.recv(1024).decode().strip().replace('\x00', '')

        if self.reread_on_query:
            self.load_data()

        response = "STRING NOT FOUND"
        if query in self.data:
            response = "STRING EXISTS"

        response += "\n"
        client_socket.send(response.encode())

        end_time = time.time()
        exec_time = (end_time - start_time) * 1000  # Execution time in milliseconds

        log_message = f"DEBUG: {addr[0]}:{addr[1]} requested '{query}' - {response.strip()} - Execution Time: {exec_time:.2f} ms\n"
        print(log_message)

        client_socket.close()

def read_config(config_file_path: str) -> str:
    """
    Read and return the 'linuxpath' setting from the config file.

    Args:
        config_file_path (str): Path to the configuration file.

    Returns:
        str: Path specified by 'linuxpath' in the configuration file.

    Raises:
        ValueError: If 'linuxpath' setting is not found in the configuration file.
    """
    config = configparser.ConfigParser()
    config.read(config_file_path)

    if 'DEFAULT' in config and 'linuxpath' in config['DEFAULT']:
        return config['DEFAULT']['linuxpath']
    else:
        raise ValueError("Configuration file does not contain 'linuxpath' setting.")

def run_server(config_file_path: str) -> None:
    """
    Run the server based on configuration settings from the specified file.

    Args:
        config_file_path (str): Path to the configuration file.
    """
    config = configparser.ConfigParser()
    config.read(config_file_path)

    use_ssl = config.getboolean('Server', 'use_ssl', fallback=True)
    port = config.getint('Server', 'port', fallback=44445)
    reread_on_query = config.getboolean('Server', 'reread_on_query', fallback=True)
    linuxpath = read_config(config_file_path)

    server = StringSearchServer(config_file_path, reread_on_query=reread_on_query, port=port, use_ssl=use_ssl)
    server.run()

if __name__ == "__main__":
    config_file_path = 'config.ini'  # Replace with your actual config file path
    run_server(config_file_path)

