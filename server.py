from flask import Flask

app = Flask(__name__)

@app.route('/status')
def status():
    return "Active"

if __name__ == '__main__':
    app.run(port=5000)
