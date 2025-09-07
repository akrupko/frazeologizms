#!/usr/bin/env python3
"""
Simple HTTP server for the phraseological units website.
Solves CORS issues in Chrome when running locally.

Usage:
    python start_server.py
    
Then open: http://localhost:8000
"""

import http.server
import socketserver
import webbrowser
import os

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_server():
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"🚀 Сервер запущен на http://localhost:{PORT}")
            print(f"📂 Обслуживается папка: {os.getcwd()}")
            print(f"🌐 Откройте http://localhost:{PORT} в любом браузере")
            print(f"⏹️  Нажмите Ctrl+C для остановки сервера")
            
            # Try to open browser automatically
            try:
                webbrowser.open(f'http://localhost:{PORT}')
                print(f"✅ Браузер открыт автоматически")
            except:
                print(f"⚠️  Откройте браузер вручную")
            
            httpd.serve_forever()
            
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