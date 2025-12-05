import os
import subprocess
import sys

# --- CONFIGURATION ---
VENV_DIR = ".venv"
REQUIREMENTS_FILE = "requirements.txt"

# --- FUNCTIONS ---

def setup_venv():
    """
    Checks for a virtual environment, creates it if it doesn't exist,
    and installs dependencies from requirements.txt.
    """
    if not os.path.exists(VENV_DIR):
        print(f"Virtual environment not found. Creating one at '{VENV_DIR}'...")
        try:
            subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)
            print("Virtual environment created successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error creating virtual environment: {e}")
            return False
    else:
        print("Virtual environment already exists.")

    print("\nInstalling dependencies from requirements.txt...")
    
    # Determine the path to the pip executable in the venv
    if sys.platform == "win32":
        pip_executable = os.path.join(VENV_DIR, "Scripts", "pip")
    else:
        pip_executable = os.path.join(VENV_DIR, "bin", "pip")

    try:
        subprocess.run([pip_executable, "install", "-r", REQUIREMENTS_FILE], check=True)
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False
    
    print(f"\nSetup complete. To activate the virtual environment, run:")
    if sys.platform == "win32":
        print(f"> .\\{VENV_DIR}\\Scripts\\activate")
    else:
        print(f"$ source {VENV_DIR}/bin/activate")
        
    return True

def main():
    """Main function to run the setup."""
    setup_venv()

if __name__ == "__main__":
    main()
