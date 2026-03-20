import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tcp_client import send_message
from http_client import GoHTTPClient


class TestTCPClient(unittest.TestCase):

    @patch('socket.socket')
    def test_send_message_success(self, mock_socket):
        mock_sock = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_sock
        mock_sock.recv.return_value = b"OK\n"

        send_message("ping")

        mock_sock.connect.assert_called_with(("localhost", 8080))
        mock_sock.sendall.assert_called_with(b"ping\n")
        mock_sock.recv.assert_called_with(1024)

    @patch('socket.socket')
    def test_send_message_connection_refused(self, mock_socket):
        mock_socket.return_value.__enter__.return_value.connect.side_effect = ConnectionRefusedError

        with patch('builtins.print') as mock_print:
            send_message("ping")
            mock_print.assert_called_with("Error: Server not running on localhost:8080")


class TestHTTPClient(unittest.TestCase):

    @patch('http_client.requests')
    def test_compute_success(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 55, "time_ms": 100.5}
        mock_requests.post.return_value = mock_response

        client = GoHTTPClient()
        result = client.compute([1, 2, 3, 4, 5])

        self.assertTrue(result["success"])
        self.assertEqual(result["result"], 55)
        self.assertEqual(result["server_time_ms"], 100.5)

    @patch('http_client.requests')
    def test_compute_connection_error(self, mock_requests):
        # Создаём исключение ConnectionError
        mock_requests.post.side_effect = Exception("ConnectionError")

        client = GoHTTPClient()
        result = client.compute([1, 2, 3])

        self.assertFalse(result["success"])
        # Проверяем, что ошибка поймана
        self.assertIn("error", result)

    @patch('http_client.requests')
    def test_compute_http_error(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_requests.post.return_value = mock_response

        client = GoHTTPClient()
        result = client.compute([1, 2, 3])

        self.assertFalse(result["success"])
        self.assertIn("HTTP 500", result["error"])


if __name__ == "__main__":
    unittest.main()