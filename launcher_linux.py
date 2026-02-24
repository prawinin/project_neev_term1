import sys
import os
import subprocess
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
BACKEND_DIR = SRC_DIR / "backend"

VENV_PYTHON = ROOT_DIR / ".venv" / "bin" / "python"
PYTHON_EXEC = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable


def main():
    print("Starting Project Neev Term 1")
    print(f"Root: {ROOT_DIR}")
    print(f"Python: {PYTHON_EXEC}")

    env = os.environ.copy()
    current_pythonpath = env.get("PYTHONPATH", "")
    new_paths = [str(BACKEND_DIR), str(SRC_DIR)]
    if current_pythonpath:
        env["PYTHONPATH"] = ":".join(new_paths) + ":" + current_pythonpath
    else:
        env["PYTHONPATH"] = ":".join(new_paths)

    processes = []

    try:
        print("\n[1/2] Starting backend (Uvicorn)...")
        backend_cmd = [
            PYTHON_EXEC,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ]
        backend_process = subprocess.Popen(backend_cmd, cwd=str(ROOT_DIR), env=env)
        processes.append(backend_process)

        time.sleep(3)

        print("[2/2] Starting frontend (Streamlit)...")
        frontend_cmd = [
            PYTHON_EXEC,
            "-m",
            "streamlit",
            "run",
            str(SRC_DIR / "frontend" / "app_term1.py"),
            "--server.address",
            "127.0.0.1",
            "--server.port",
            "8501",
        ]
        frontend_process = subprocess.Popen(frontend_cmd, cwd=str(ROOT_DIR), env=env)
        processes.append(frontend_process)

        print("\nServices are running. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down...")
        for process in processes:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        sys.exit(0)


if __name__ == "__main__":
    main()
