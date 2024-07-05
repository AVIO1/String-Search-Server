import argparse
import configparser
from server_script import StringSearchServer

def read_config(config_file_path):
    """
    Reads the configuration file and retrieves the server settings.

    Args:
        config_file_path (str): Path to the configuration file.

    Returns:
        dict: Dictionary containing server configuration settings.
    """
    config = configparser.ConfigParser()
    config.read(config_file_path)

    # Read server configuration settings
    server_config = {
        'linuxpath': config.get('Server', 'linuxpath', fallback=''),
        'reread_on_query': config.getboolean('Server', 'reread_on_query', fallback=True),
        'port': config.getint('Server', 'port', fallback=8000),
        'use_ssl': config.getboolean('Server', 'use_ssl', fallback=True)
    }

    return server_config

def main(config_file_path):
    """
    Main function to initialize and start the String Search Server.

    Args:
        config_file_path (str): Path to the configuration file.

    """
    # Read server configuration
    server_config = read_config(config_file_path)

    # Start the server
    server = StringSearchServer(
        config_file_path=config_file_path,
        reread_on_query=server_config['reread_on_query'],
        port=server_config['port'],
        use_ssl=server_config['use_ssl']
    )

    server.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="String Search Server")
    parser.add_argument("--config", required=True, help="Path to config file (e.g., config.env)")
    args = parser.parse_args()

    main(args.config)
