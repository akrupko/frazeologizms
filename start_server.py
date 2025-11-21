#!/usr/bin/env python3
"""
Flask application server for the phraseological units website.

Usage:
    python start_server.py
    
Then open: http://localhost:5000
"""

import os
import webbrowser
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env file
load_dotenv()

PORT = int(os.getenv('FLASK_PORT', 5000))
HOST = os.getenv('FLASK_HOST', '127.0.0.1')

def start_server():
    """Start the Flask development server."""
    app = create_app()
    
    try:
        print(f"🚀 Flask сервер запущен на http://{HOST}:{PORT}")
        print(f"📂 Приложение: Тренажер фразеологизмов")
        print(f"🌐 Откройте http://{HOST}:{PORT} в любом браузере")
        print(f"⏹️  Нажмите Ctrl+C для остановки сервера")
        
        # Try to open browser automatically
        try:
            webbrowser.open(f'http://{HOST}:{PORT}')
            print(f"✅ Браузер открыт автоматически")
        except:
            print(f"⚠️  Откройте браузер вручную")
        
        app.run(host=HOST, port=PORT, debug=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Порт {PORT} уже используется")
            print(f"💡 Попробуйте другой порт или закройте другие серверы")
        else:
            print(f"❌ Ошибка запуска сервера: {e}")

if __name__ == "__main__":
    start_server()
