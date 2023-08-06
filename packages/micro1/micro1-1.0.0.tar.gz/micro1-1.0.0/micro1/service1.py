#!flask/bin/python
from flask import Flask

port_num = 9111

app = Flask(__name__)

@app.route('/ms')
def index():
    return "Hello, World! this is micro servce 1 \n"

if __name__ == '__main__':
    app.run(host='192.168.1.3',port=port_num,debug=True)
