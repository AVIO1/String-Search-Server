import time
import socket
import subprocess
from typing import Callable, Any, List
import configparser
import pytest
from rabin_karp_search import rabin_karp_search
from binary_search import binary_search
from kmp_search import kmp_search
from brute_force_search import brute_force_search
from aho_corasick_search import aho_corasick_search


def read_config(config_file_path: str, section: str, key: str) -> str:
    """
    Reads a specific key from a section in the configuration file.
    Returns:
        str: Value of the key in the configuration file.
    Raises:
        ValueError: If the key is not found in the specified section.
    """
    config = configparser.ConfigParser()
    config.read(config_file_path)

    if section in config and key in config[section]:
        return config[section][key]
    else:
        raise ValueError(f"Configuration file does not contain '{key}' setting in '{section}' section.")


def measure_execution_time(search_func: Callable[..., None], *args: Any) -> float:
    """
    Measure the execution time of a search function.
    Returns:
        float: Execution time in milliseconds.
    """
    start_time = time.time()
    search_func(*args)
    end_time = time.time()
    return (end_time - start_time) * 1000  # Convert to milliseconds


def calculate_average_time(search_func: Callable[..., None], data: Any, queries: List[str], iterations: int = 100) -> float:
    """
    Calculate the average execution time of a search function over multiple iterations.

    Args:
        search_func (Callable): The search function to measure.
        data (Any): The data to search within.
        queries (List[str]): List of queries to search for.
        iterations (int, optional): Number of iterations to perform. Defaults to 100.

    Returns:
        float: Average execution time in milliseconds.
    """
    total_time = 0
    for _ in range(iterations):
        for query in queries:
            total_time += measure_execution_time(search_func, data, query)
    return total_time / (iterations * len(queries))


class TestAlgorithms:
    def __init__(self, config_file_path: str):
        self.data = None

    # Your existing initialization code

    # Your existing test methods

    def test_server_search(self) -> None:
        """
        Test server search functionality.
        """
        server_address = ('135.181.96.160', 44445)
        queries = ["query_string_1", "query_string_2", "query_string_3"]  # Example queries to test

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(server_address)

            for query in queries:
                query_bytes = query.encode('utf-8')
                sock.sendall(query_bytes)

                response = sock.recv(1024).decode('utf-8').strip()

                if "String found" in response:
                    assert True, f"Query '{query}' found in server response"
                elif "String not found" in response:
                    assert False, f"Query '{query}' not found in server response"
                else:
                    assert False, f"Unexpected response from server: {response}"

    def test_rabin_karp_search(self) -> None:
        """
        Test Rabin-Karp search algorithm.
        """
        for query in self.queries:
            assert rabin_karp_search(self.test_file_path, query), f"Query '{query}' should be found in the dataset"

    def test_binary_search(self) -> None:
        """
        Test Binary search algorithm.
        """
        for query in self.queries:
            if query in self.data:
                assert binary_search(self.sorted_data, query), f"Query '{query}' should be found in the dataset"
            else:
                assert not binary_search(self.sorted_data, query), f"Query '{query}' should not be found in the dataset"

    def test_kmp_search(self) -> None:
        """
        Test Knuth-Morris-Pratt (KMP) search algorithm.
        """
        for query in self.queries:
            if query in ''.join(self.data):
                assert kmp_search(''.join(self.data), query), f"Query '{query}' should be found in the dataset"
            else:
                assert not kmp_search(''.join(self.data), query), f"Query '{query}' should not be found in the dataset"

    def test_brute_force_search(self) -> None:
        """
        Test Brute Force search algorithm.
        """
        for query in self.queries:
            if query in ''.join(self.data):
                assert brute_force_search(''.join(self.data), query), f"Query '{query}' should be found in the dataset"
            else:
                assert not brute_force_search(''.join(self.data), query), f"Query '{query}' should not be found in the dataset"

    def test_aho_corasick_search(self) -> None:
        """
        Test Aho-Corasick search algorithm.
        """
        patterns = ["1;0;1;28;0;7;5;0", "10;0;1;26;0;8;3;0", "18;0;6;28;0;23;5;0"]
        assert aho_corasick_search(''.join(self.data), patterns), "All patterns should be found in the dataset"

    def test_subprocess_search_found(self, tmp_path) -> None:
        """
        Test case to check if the search process finds the pattern in the sample text file using subprocess.
        """
        text_file = tmp_path / "test_file.txt"
        with open(text_file, 'w') as f:
            f.write("\n".join(self.data))

        pattern = "13;0;1;28;0;7;4;0;"  # Example pattern to search
        process = subprocess.Popen(['python', 'process.py', str(text_file), pattern],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        assert f"Pattern '{pattern}' found in '{text_file}'." in stdout.decode('utf-8')

    def test_subprocess_search_not_found(self, tmp_path) -> None:
        """
        Test case to check if the search process does not find the pattern in the sample text file using subprocess.
        """
        text_file = tmp_path / "test_file.txt"
        with open(text_file, 'w') as f:
            f.write("\n".join(self.data))

        pattern = "6;0;1;16;0;7;5;0;"  # Non-existent pattern
        process = subprocess.Popen(['python', 'process.py', str(text_file), pattern],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        assert f"Pattern '{pattern}' not found in '{text_file}'." in stdout.decode('utf-8')

    def test_measure_execution_time(self) -> None:
        """
        Test measure_execution_time function.
        """
        execution_time = measure_execution_time(rabin_karp_search, self.test_file_path, self.queries[0])
        assert isinstance(execution_time, float), "Execution time should be a float"

    def test_calculate_average_time(self) -> None:
        """
        Test calculate_average_time function.
        """
        average_time = calculate_average_time(rabin_karp_search, self.data, self.queries)
        assert isinstance(average_time, float), "Average time should be a float"


if __name__ == '__main__':
    pytest.main()
