"""Flask Setup File
This file will setup Flask with CORS be enable remote requests
"""

from flask import Flask
from flask_caching import Cache

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "super secret key"

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

from app import views