from flask import Flask, render_template, jsonify, request
from threading import Thread
import time

from autoclicker import AutoClicker

app = Flask(__name__)
clicker = AutoClicker()
clicker.set_dry_run(True)  # safety: default to dry-run when controlled via web
clicker.start()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/status')
def status():
    return jsonify({'running': clicker.running})


@app.route('/toggle', methods=['POST'])
def toggle():
    clicker.toggle()
    return jsonify({'running': clicker.running})


def run_app(host='127.0.0.1', port=5000):
    app.run(host=host, port=port, debug=False)


if __name__ == '__main__':
    run_app()
