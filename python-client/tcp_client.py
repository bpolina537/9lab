import socket


def send_message(message="ping"):
    try:
        # Подключаемся к серверу
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(("localhost", 8080))

            # Отправляем сообщение
            sock.sendall(f"{message}\n".encode())

            # Получаем ответ
            response = sock.recv(1024).decode()
            print(f"Sent: {message}")
            print(f"Received: {response.strip()}")

    except ConnectionRefusedError:
        print("Error: Server not running on localhost:8080")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Можно менять сообщение
    send_message("hello")