#!flask/bin/python
from flask import Flask

# app = Flask(__name__)

# set the "static" directory as the static folder.
# this will ensure that all the static files are under one folder
app = Flask(__name__, static_url_path='/test')

# serving some static html files
@app.route('/html/path:path')
def send_html(path):
    return {'data' : "manmohan"}

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=4000,debug=False)
