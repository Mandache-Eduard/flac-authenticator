import shutil
import subprocess

def call_spek(file_path):
    if not shutil.which("spek"):
        print("Spek not detected. Please install it from https://spek.cc and ensure it's in your PATH.")
    # Run Spek via command line
    try:
        subprocess.run(["spek", file_path], check=True)
    except FileNotFoundError:
        print("Spek is not installed or not in your PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Spek exited with an error: {e}")