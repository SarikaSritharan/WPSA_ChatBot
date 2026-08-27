from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

# Ensure the backend directory is in the path so local imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Path helper for PyInstaller standalone EXE
def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    # Project root is two levels up from this file (backend/app.py)
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), relative_path)

# Correctly locate folders
data_dir = get_resource_path('backend/data')
frontend_dir = get_resource_path('frontend')

try:
    # This works at runtime and for the EXE
    from ai_engine import AyuAI
    from translator_handler import TranslatorHandler
except (ImportError, ModuleNotFoundError):
    # This makes the IDE (VS Code/Pylance) happy
    from backend.ai_engine import AyuAI
    from backend.translator_handler import TranslatorHandler

app = Flask(__name__, static_folder=frontend_dir)
CORS(app)

# Initialize AI
ai = AyuAI(data_dir)
translator = TranslatorHandler()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    lang = data.get('lang', 'en') # 'en', 'si', or 'ta'
    
    # 1. Translate user message to English if needed
    english_message = translator.translate_to_english(user_message, lang)
    
    # 2. Get AI response in English
    english_response = ai.get_response(english_message)
    
    # 3. Translate response back to user's language
    translated_response = translator.translate_from_english(english_response, lang)
    
    return jsonify({
        "response": translated_response,
        "original_message": user_message,
        "intent_detected": ai.detect_intent(english_message),
        "emotion_detected": ai.detect_emotion(english_message)
    })

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(app.static_folder, 'static'), path)

if __name__ == '__main__':
    # Automatically open browser when running as a standalone EXE
    if getattr(sys, 'frozen', False):
        import webbrowser
        import threading
        def open_browser():
            import time
            time.sleep(1.5) # Wait for Flask to start
            webbrowser.open('http://127.0.0.1:5000')
        threading.Thread(target=open_browser).start()
        
    app.run(debug=False, port=5000)
