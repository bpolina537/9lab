import requests
import time


class GoHTTPClient:
    def __init__(self, base_url="http://localhost:8081"):
        self.base_url = base_url

    def compute(self, numbers):
        url = f"{self.base_url}/compute"
        data = {"numbers": numbers}

        try:
            start = time.time()
            response = requests.post(url, json=data, timeout=30)
            elapsed = (time.time() - start) * 1000

            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "result": result["result"],
                    "server_time_ms": result["time_ms"],
                    "client_time_ms": elapsed
                }
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}

        except Exception as e:
            # Ловим любые исключения (ConnectionError, Timeout, etc.)
            error_msg = str(e)
            if "Connection refused" in error_msg or "connection" in error_msg.lower():
                return {"success": False, "error": "Server not running on port 8081"}
            return {"success": False, "error": error_msg}


if __name__ == "__main__":
    client = GoHTTPClient()

    numbers = [1, 2, 3, 4, 5]
    print(f"Testing with: {numbers}")
    result = client.compute(numbers)

    if result["success"]:
        print(f"Result: {result['result']}")
        print(f"Server time: {result['server_time_ms']:.2f} ms")
        print(f"Client time: {result['client_time_ms']:.2f} ms")
    else:
        print(f"Error: {result['error']}")