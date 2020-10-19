import flask
from flask import *
import threading

import logging

app = flask.Flask('Project Zero')

log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True

@app.route('/', methods=['GET', 'POST'])
def home():
    return 'pong! project zero is up :)'

def start():
    app.run(host="0.0.0.0", port="3000")

t = threading.Thread(target=start)

t.start()