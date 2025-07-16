import os
import sys
from threading import Thread
from main_app.app import app as main_app
from crm_app.crm_app import app as crm_app

def initialize_database():
    """Initialize the database"""
    print("Initializing database...")
    import subprocess
    subprocess.run([sys.executable, 'init_db.py'])

def run_crm_app():
    """Run CRM app on port 5001"""
    crm_app.run(host='0.0.0.0', port=5001, debug=False)

if __name__ == '__main__':
    print("Starting Booking System...")
    
    # Initialize database
    initialize_database()
    
    # Start CRM app in background thread
    crm_thread = Thread(target=run_crm_app)
    crm_thread.daemon = True
    crm_thread.start()
    
    # Run main app on Railway's PORT
    port = int(os.environ.get('PORT', 5000))
    main_app.run(host='0.0.0.0', port=port, debug=False)