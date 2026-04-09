import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    version = os.getenv("VERSION", "UNKNOWN")
    return f"Hello from {version} deployment!"

@app.route('/health')
def health():
    return "OK", 200

app.run(host='0.0.0.0', port=5000)