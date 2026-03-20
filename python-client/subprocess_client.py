import subprocess
import os
import sys


def run_go_binary():
    # Определяем путь к бинарнику в зависимости от ОС
    if sys.platform == "win32":
        binary_path = os.path.join("..", "go-binary", "go-binary.exe")
    else:
        binary_path = os.path.join("..", "go-binary", "go-binary")

    try:
        result = subprocess.run(
            [binary_path],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Output from Go: {result.stdout.strip()}")
    except FileNotFoundError:
        print(f"Error: Binary not found at {binary_path}")
        print("Please run build script first (build.bat or build.sh)")
    except subprocess.CalledProcessError as e:
        print(f"Error running binary: {e}")
        print(f"stderr: {e.stderr}")


if __name__ == "__main__":
    run_go_binary()