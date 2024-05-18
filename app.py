import logging

from flask import Flask
from flask_cors import CORS

from controller import controller

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Enable CORS
app.register_blueprint(controller)

# Inits

