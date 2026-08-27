import PyInstaller.__main__
import os
import sys

# Increase recursion depth for complex packaging
sys.setrecursionlimit(5000)

# Build the Ayu AI Standalone Executable
PyInstaller.__main__.run([
    'backend/app.py',
    '--name=AyuAI',
    '--onefile',
    '--noconsole',
    '--noupx',  # Disable UPX to fix "Ordinal Not Found" errors
    '--clean',  # Clean cache before building
    '--add-data=backend/data;backend/data',
    '--add-data=frontend;frontend',
    '--icon=frontend/static/images/ayu_profile.png',
    '--hidden-import=flask',
    '--hidden-import=flask_cors',
    '--hidden-import=mtranslate',
])

print("\n--- Build Complete! ---")
print("Your standalone executable is located in the 'dist' folder.")
print("You can now share 'AyuAI.exe' with anyone!")
