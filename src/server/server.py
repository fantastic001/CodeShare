# coding: UTF-8

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def about():
    return "Telenor Bot"



@app.route('/webhook/', methods=['POST'])
def main():
    data = request.get_json()
    messaging_events = data['entry'][0]['messaging']

    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
