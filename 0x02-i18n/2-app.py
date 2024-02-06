#!/usr/bin/env python3
"""
Basic Flask app with Babel setup and locale selector
"""

from flask import Flask, render_template, request
from flask_babel import Babel, _


app = Flask(__name__)


class Config:
    """Config class for setting up Babel"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Determine the best-matching locale for the client"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index() -> str:
    """Render index.html template"""
    return render_template('2-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
