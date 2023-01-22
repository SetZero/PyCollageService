"""Flask Setup File
This file will setup Flask with CORS be enable remote requests
"""

from flask import Flask

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "super secret key"

from app import views