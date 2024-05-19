import logging
from flask import Flask
from flask_cors import CORS

from controller import controller

app = Flask(__name__)
# Set up CORS not just to allow all origins but also to allow Content-Type header, methods, etc.
CORS(app, resources={r"/api/*": {"origins": "*", "allow_headers": [
     "Content-Type", "Authorization"], "methods": ["GET", "POST", "OPTIONS"]}})


# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Register the blueprint
app.register_blueprint(controller)

# Start the application
if __name__ == "__main__":
    app.run(debug=True)
