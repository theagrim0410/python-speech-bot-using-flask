from flask import Flask, render_template
import subprocess
import os
import signal

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('html.html')


@app.route('/run-script')
def run_script():
    output = subprocess.run(['python', 'speech_gui.py'],
                            capture_output=True, text=True)
    return output.stdout or "Script executed!"


@app.route('/shutdown')
def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return "Shutting down server..."


if __name__ == '__main__':
    app.run(debug=True)
