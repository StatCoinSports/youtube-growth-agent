from flask import Flask, request, jsonify
import os
from utils.youtube import get_subscribers

app = Flask(__name__)

@app.route('/')
def home():
    return 'YouTube Growth Agent is Live'

@app.route('/stats')
def stats():
    data = get_subscribers()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)