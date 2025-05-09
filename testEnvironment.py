import os
import sys
import venv
import subprocess

REQUIRED_PYTHON = "python3"
VENV_DIR = "venv"

def check_python_version():
    system_major = sys.version_info.major
    if REQUIRED_PYTHON == "python":
        required_major = 2
    elif REQUIRED_PYTHON == "python3":
        required_major = 3
    else:
        raise ValueError("Unrecognized python interpreter: {}".format(
            REQUIRED_PYTHON))

    if system_major != required_major:
        raise TypeError(
            "This project requires Python {}. Found: Python {}".format(
                required_major, sys.version))
    else:
        print(">>> Development environment passes all tests!")

def create_virtualenv():
    if not os.path.isdir(VENV_DIR):
        print(f">>> Creating virtual environment in ./{VENV_DIR}")
        venv.create(VENV_DIR, with_pip=True)
        print(">>> Virtual environment created.")
    else:
        print(f">>> Virtual environment already exists in ./{VENV_DIR}")


def install_requirements():
    requirements_file = "requirements.txt"
    if os.path.exists(requirements_file):
        try:
            print(">>> Installing dependencies from requirements.txt...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
            print(">>> Dependencies installed successfully.")
        except subprocess.CalledProcessError:
            print("!!! Failed to install dependencies.")
            sys.exit(1)
    else:
        print("!!! requirements.txt not found.")
        sys.exit(1)

def main():
    check_python_version()
    create_virtualenv()
    install_requirements()

    print("\n>>> Setup complete!")
    print(f"To activate the virtual environment, run:\n")
    if os.name == 'nt':
        print(f"    {VENV_DIR}\\Scripts\\activate")
    else:
        print(f"    source {VENV_DIR}/bin/activate")


if __name__ == '__main__':
    main()