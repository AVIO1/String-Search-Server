import socket
import threading
import ssl
import configparser
import subprocess
import pytest
from server_script import StringSearchServer


def handle_client(conn: socket.socket, addr: tuple, use_ssl: bool = False) -> None:
    """
    Handles a client connection, optionally using SSL for secure communication.

    Args:
        conn (socket.socket): The socket object for the client connection.
        addr (tuple): The address of the client.
        use_ssl (bool, optional): Flag indicating whether to use SSL for the connection. Defaults to False.
    """
    if use_ssl:
        # SSL wrapping
        conn = ssl.wrap_socket(
            conn,
            server_side=True,
            certfile="server.crt",
            keyfile="server.key",
            ssl_version=ssl.PROTOCOL_TLS
        )

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
    finally:
        conn.close()


def read_config(config_file_path: str) -> str:
    """
    Reads the configuration file and retrieves the 'Linux path' value from the DEFAULT section.

    """
    config = configparser.ConfigParser()
    config.read(config_file_path)

    if 'DEFAULT' in config and 'Linux Path' in config['DEFAULT']:
        return config['DEFAULT']['Linux path']
    else:
        raise ValueError("Configuration file does not contain 'Linux Path' setting in DEFAULT section.")


def run_server(port: int, use_ssl: bool = False) -> None:
    """
    Runs the server based on the provided configuration settings.

    Args:
        port (int): Port number on which the server should listen.
        use_ssl (bool, optional): Flag indicating whether to use SSL for the server. Defaults to False.
    """
    server = StringSearchServer(
        config_file_path="config.ini",
        reread_on_query=False,  # Example value, adjust as needed
        port=port,
        use_ssl=use_ssl
    )

    server_thread = threading.Thread(target=server.run)
    server_thread.daemon = True
    server_thread.start()

    print(f"Server started on port {port} with SSL: {use_ssl}")

    # Keep the main thread running to keep the server alive
    try:
        while True:
            continue
    except KeyboardInterrupt:
        print("Server stopped by user.")
        server.server_socket.close()


@pytest.fixture
def start_server() -> None:
    """
    Fixture to start the server for testing purposes.

    Yields:
        None
    """
    server_thread = threading.Thread(target=run_server, args=(44445, False))
    server_thread.daemon = True
    server_thread.start()
    yield
    # Clean-up code if needed after the server stops


def test_string_exists(start_server: None) -> None:
    """
    Test case to check if the server correctly responds with "STRING EXISTS".

    Args:
        start_server: Fixture to start the server.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('135.181.96.160', 44445))
    client_socket.send(b"example_string")
    response = client_socket.recv(1024).decode().strip()
    assert response == "STRING EXISTS"
    client_socket.close()


def test_string_not_found(start_server: None) -> None:
    """
    Test case to check if the server correctly responds with "STRING NOT FOUND".

    Args:
        start_server: Fixture to start the server.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('135.181.96.160', 44445))
    client_socket.send(b"nonexistent_string")
    response = client_socket.recv(1024).decode().strip()
    assert response == "STRING NOT FOUND"
    client_socket.close()


@pytest.fixture
def test_file_path() -> str:
    """
    Fixture to provide path to a sample text file for subprocess tests.

    Returns:
        str: Path to the sample text file.
    """
    return 'Path to the sample text file.'


def test_subprocess_search_found(start_server: None, test_file_path: str) -> None:
    """
    Test case to check if the search process finds the pattern in the sample text file using subprocess.

    Args:
        start_server: Fixture to start the server.
        test_file_path: Fixture providing path to the sample text file.
    """
    pattern = "13;0;1;28;0;7;4;0;"  # Example pattern to search
    process = subprocess.Popen(['python', 'process.py', test_file_path, pattern],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    assert f"Pattern '{pattern}' found in '{test_file_path}'." in stdout.decode('utf-8')


def test_subprocess_search_not_found(start_server: None, test_file_path: str) -> None:
    """
    Test case to check if the search process does not find the pattern in the sample text file using subprocess.

    Args:
        start_server: Fixture to start the server.
        test_file_path: Fixture providing path to the sample text file.
    """
    pattern = "6;0;1;16;0;7;5;0;"  # Non-existent pattern
    process = subprocess.Popen(['python', 'process.py', test_file_path, pattern],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    assert f"Pattern '{pattern}' not found in '{test_file_path}'." in stdout.decode('utf-8')
