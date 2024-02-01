from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/command', methods=['POST'])
def command():
    command = request.json['command']
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        output = f'Error: {e}'

    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
