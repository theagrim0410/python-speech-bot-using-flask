from flask import Flask, render_template, request
import subprocess
import os
import signal
import sys

app = Flask(__name__)

# Process handle for the background speech script
process = None


@app.route('/')
def home():
    return render_template('html.html')


@app.route('/run-script')
def run_script():
    """Start speech_gui.py in the background (non-blocking).

    Returns immediately so the browser does not wait while the speech
    recognition runs.
    """
    global process
    if process and process.poll() is None:
        return "Script is already running."

    script_path = os.path.join(os.path.dirname(__file__), 'speech_gui.py')

    # Use the same Python interpreter that's running the Flask app
    try:
        process = subprocess.Popen([sys.executable, script_path],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   text=True)
    except Exception as e:
        return f"Failed to start script: {e}"

    return "Script started."


@app.route('/stop-script')
def stop_script():
    """Terminate the background speech script if it's running."""
    global process
    if process and process.poll() is None:
        try:
            process.terminate()
            return "Script termination requested."
        except Exception as e:
            return f"Failed to terminate script: {e}"
    return "No running script."


@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    """Attempt a graceful shutdown using Werkzeug; fallback to kill."""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        # Fallback for environments where werkzeug shutdown is not exposed
        try:
            os.kill(os.getpid(), signal.SIGTERM)
        except Exception:
            pass
        return "Server shutting down (fallback)."
    func()
    return "Shutting down server..."


if __name__ == '__main__':
    # Disable the reloader to avoid double-starting subprocesses
    app.run(debug=True, use_reloader=False)
