#!/usr/bin/env python3
"""
Basic Flask app with Babel setup, locale selector using user preferences,
parametrized templates, support for user login emulation,
and infer appropriate time zone
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz


app = Flask(__name__)


class Config:
    """Config class for setting up Babel"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app)


# Mock user table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id):
    """Return user dictionary based on user ID"""
    return users.get(user_id)


@app.before_request
def before_request():
    """Set user in global flask.g object"""
    user_id = request.args.get('login_as')
    g.user = get_user(int(user_id)) if user_id else None


@babel.localeselector
def get_locale():
    """Determine the best-matching locale for the client"""
    if 'locale' in request.args:
        locale = request.args.get('locale')
        if locale in app.config['LANGUAGES']:
            return locale
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """Determine the appropriate time zone for the client"""
    if 'timezone' in request.args:
        timezone = request.args.get('timezone')
        try:
            pytz.timezone(timezone)
            return timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    if g.user and g.user['timezone']:
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index():
    """Render index.html template"""
    return render_template('7-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
