#!flask/bin/python
from flask import Flask, jsonify

# app = Flask(__name__)

# set the "static" directory as the static folder.
# this will ensure that all the static files are under one folder
app = Flask(__name__)

# serving some static html files
@app.route('/')
def dummy():
    return jsonify({'data' : "manmohan"})

if __name__ == '__main__':
    app.run()
