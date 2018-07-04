import os

from flask import Flask

# create and configure the app
app = Flask(__name__, instance_relative_config=True)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

@app.route('/hello')
def hello():
    return 'Hello, World!'

