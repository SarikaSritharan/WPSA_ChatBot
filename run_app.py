import subprocess
import time
import webbrowser
import os
import sys

def run_project():
    print("Starting Ayu AI Wedding Planner...")
    
    # Path to the backend
    backend_path = os.path.join(os.path.dirname(__file__), 'backend', 'app.py')
    
    # Start the Flask server in a separate process
    try:
        flask_process = subprocess.Popen([sys.executable, backend_path])
        print("Flask server started at http://127.0.0.1:5000")
        
        # Give it a moment to start
        time.sleep(2)
        
        # Open the frontend in the default browser
        frontend_path = os.path.join(os.path.dirname(__file__), 'frontend', 'index.html')
        print(f"Opening frontend: {frontend_path}")
        webbrowser.open('file://' + os.path.abspath(frontend_path))
        
        print("\nProject is running! Press Ctrl+C in this terminal to stop.")
        
        # Keep the script alive while the flask process is running
        flask_process.wait()
        
    except KeyboardInterrupt:
        print("\nStopping Ayu AI...")
        flask_process.terminate()
    except Exception as e:
        print(f"Error starting project: {e}")

if __name__ == "__main__":
    run_project()
