import os
import sys
import subprocess
import webbrowser
import time
from threading import Thread

def run_main_app():
    """Run the main Flask application"""
    main_app_path = os.path.join(os.getcwd(), 'main_app', 'app.py')
    subprocess.run([sys.executable, main_app_path])

def run_crm_app():
    """Run the CRM Flask application"""
    crm_app_path = os.path.join(os.getcwd(), 'crm_app', 'crm_app.py')
    subprocess.run([sys.executable, crm_app_path])

def open_browser():
    """Open browser after a delay"""
    time.sleep(2)  # Wait for servers to start
    webbrowser.open('http://localhost:5000')
    print("Opening browser to http://localhost:5000")
    time.sleep(1)  # Wait a bit more
    webbrowser.open('http://localhost:5001')
    print("Opening browser to http://localhost:5001")

def initialize_database():
    """Initialize the database"""
    print("Initializing database...")
    subprocess.run([sys.executable, 'init_db.py'])

if __name__ == '__main__':
    print("Starting Booking System...")
    
    # Initialize database
    initialize_database()
    
    # Start CRM app in a separate thread
    crm_thread = Thread(target=run_crm_app)
    crm_thread.daemon = True
    crm_thread.start()
    print("CRM application started on http://localhost:5001")
    
    # Open browser after a delay
    browser_thread = Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Run main app in the main thread
    print("Main application starting on http://localhost:5000")
    run_main_app()