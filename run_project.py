#!/usr/bin/env python3
import os
import subprocess
import sys
import platform
import venv
import webbrowser
import time
from pathlib import Path

def run_command(command, cwd=None, env=None):
    """Execute a shell command and print its output"""
    print(f"Running: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            check=True,
            text=True,
            capture_output=True
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command)}")
        print(f"Error message: {e.stderr}")
        return False

def detect_python_command():
    """Detect which python command to use (python or python3)"""
    if platform.system() == "Windows":
        try:
            subprocess.run(["python", "--version"], check=True, capture_output=True)
            return "python"
        except:
            print("Python command not found. Please ensure Python is installed.")
            sys.exit(1)
    else:
        # Try python3 first on Unix-like systems
        try:
            subprocess.run(["python3", "--version"], check=True, capture_output=True)
            return "python3"
        except:
            try:
                subprocess.run(["python", "--version"], check=True, capture_output=True)
                return "python"
            except:
                print("Neither python3 nor python commands found. Please ensure Python is installed.")
                sys.exit(1)

def get_activated_env(venv_dir):
    """Create environment variables for an activated virtual environment"""
    env = os.environ.copy()
    
    if platform.system() == "Windows":
        env["PATH"] = str(venv_dir / "Scripts") + os.pathsep + env["PATH"]
    else:
        env["PATH"] = str(venv_dir / "bin") + os.pathsep + env["PATH"]
    
    # Clear PYTHONHOME if it exists as it can interfere with venv
    if "PYTHONHOME" in env:
        del env["PYTHONHOME"]
        
    # Set VIRTUAL_ENV environment variable
    env["VIRTUAL_ENV"] = str(venv_dir)
    
    return env

def main():
    # Get the current directory
    current_dir = Path.cwd()
    python_cmd = detect_python_command()
    
    # Step 1: Create a virtual environment
    print("\n=== Step 1: Creating virtual environment ===")
    venv_dir = current_dir / "venv"
    
    if not venv_dir.exists():
        print(f"Creating virtual environment at {venv_dir}")
        venv.create(venv_dir, with_pip=True)
    else:
        print(f"Virtual environment already exists at {venv_dir}")
    
    # Determine the path to the virtual environment's Python interpreter and activate it
    if platform.system() == "Windows":
        venv_python = venv_dir / "Scripts" / "python.exe"
        venv_pip = venv_dir / "Scripts" / "pip.exe"
    else:
        venv_python = venv_dir / "bin" / "python"
        venv_pip = venv_dir / "bin" / "pip"
    
    # Activate the virtual environment by setting up the environment variables
    print("Activating virtual environment...")
    activated_env = get_activated_env(venv_dir)
    
    # Step 2: Install backend and frontend dependencies
    print("\n=== Step 2: Installing dependencies ===")
    
    # Backend setup - updated directory structure
    backend_dir = current_dir / "backend"
    if not backend_dir.exists():
        print(f"Error: Backend directory '{backend_dir}' not found!")
        sys.exit(1)
    
    # Find the ems directory inside backend
    ems_dir = backend_dir / "ems"
    if not ems_dir.exists():
        print(f"Error: 'ems' directory not found in '{backend_dir}'")
        sys.exit(1)
    
    print(f"Found backend directory structure: {backend_dir} -> {ems_dir}")
    
    # Find the manage.py file in the ems directory
    manage_py = ems_dir / "manage.py"
    if not manage_py.exists():
        print(f"Error: manage.py not found in {ems_dir}")
        sys.exit(1)
    
    # Install backend requirements
    requirements_file = ems_dir / "requirements.txt"
    if requirements_file.exists():
        print("Installing backend requirements...")
        if not run_command([str(venv_pip), "install", "-r", str(requirements_file)], env=activated_env):
            print("Failed to install backend requirements")
            sys.exit(1)
    else:
        # Try looking for requirements.txt in the backend directory
        requirements_file = backend_dir / "requirements.txt"
        if requirements_file.exists():
            print("Installing backend requirements...")
            if not run_command([str(venv_pip), "install", "-r", str(requirements_file)], env=activated_env):
                print("Failed to install backend requirements")
                sys.exit(1)
        else:
            print(f"Warning: requirements.txt not found in {ems_dir} or {backend_dir}")
    
    # Frontend setup - updated directory structure
    frontend_dir = current_dir / "frontend"
    if not frontend_dir.exists():
        print(f"Error: Frontend directory '{frontend_dir}' not found!")
        sys.exit(1)
    
    # Install frontend dependencies
    print("Installing frontend dependencies...")
    if not run_command(["npm", "install"], cwd=frontend_dir):
        print("Failed to install frontend dependencies")
        sys.exit(1)
    
    # Step 3: Run migrations and start backend server
    print("\n=== Step 3: Setting up and starting Django backend ===")
    
    # Run migrations
    django_dir = ems_dir  # The directory containing manage.py
    print(f"Running Django migrations in {django_dir}")
    
    if not run_command([str(venv_python), str(manage_py), "makemigrations"], cwd=django_dir, env=activated_env):
        print("Failed to make migrations")
        sys.exit(1)
    
    if not run_command([str(venv_python), str(manage_py), "migrate"], cwd=django_dir, env=activated_env):
        print("Failed to apply migrations")
        sys.exit(1)
    
    # Step 4: Start backend and frontend servers
    print("\n=== Step 4: Starting the servers ===")
    
    # Start Django server in a separate process
    print("Starting Django server...")
    django_process = subprocess.Popen(
        [str(venv_python), str(manage_py), "runserver"],
        cwd=django_dir,
        env=activated_env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    
    # Start frontend server
    print("Starting React frontend...")
    try:
        frontend_process = subprocess.Popen(
            ["npm", "start"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        
        print("\n=== Both servers are now running ===")
        print("Django backend is running at http://localhost:8000/")
        print("React frontend should start shortly")
        
        # Step 5: Open the frontend in the browser
        print("\n=== Step 5: Opening frontend in browser ===")
        # Wait a moment for the servers to fully start
        time.sleep(5)
        
        frontend_url = "http://localhost:5173"
        print(f"Opening {frontend_url} in your default browser...")
        webbrowser.open(frontend_url)
        
        print("Press Ctrl+C to stop both servers")
        
        # Wait for user to interrupt
        try:
            while True:
                # Print output from both processes
                if django_process.stdout:
                    line = django_process.stdout.readline()
                    if line:
                        print(f"[Django] {line.strip()}")
                
                if frontend_process.stdout:
                    line = frontend_process.stdout.readline()
                    if line:
                        print(f"[React] {line.strip()}")
        except KeyboardInterrupt:
            print("Shutting down servers...")
            django_process.terminate()
            frontend_process.terminate()
            
    except Exception as e:
        print(f"Error starting servers: {e}")
        if 'django_process' in locals():
            django_process.terminate()
        sys.exit(1)

if __name__ == "__main__":
    main()