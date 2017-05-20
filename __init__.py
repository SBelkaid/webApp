from .webApp import app
from flask import Flask
from .webApp.views import profile

app = Flask(__name__)
app.register_blueprint(profile)
