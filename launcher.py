#!/usr/bin/env python3
"""
Launcher script for SKUD system.
Ensures dependencies are installed, initializes database, and starts the GUI.
"""

import sys
import subprocess

def install_dependencies():
    """Install required dependencies if not present."""
    try:
        import openpyxl
        print("openpyxl is already installed.")
    except ImportError:
        print("Installing openpyxl...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
            print("openpyxl installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install openpyxl: {e}")
            sys.exit(1)

def initialize_database():
    """Initialize the database."""
    try:
        from db.init_db import init_db
        init_db()
        print("Database initialized.")
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        sys.exit(1)

def run_gui():
    """Run the GUI application."""
    try:
        from gui import main
        main()
    except Exception as e:
        print(f"Failed to run GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Launching SKUD system...")
    install_dependencies()
    initialize_database()
    print("Starting GUI...")
    run_gui()
