import os
from flask import Flask, render_template, url_for, current_app
import json
from markupsafe import Markup
from dotenv import load_dotenv

from . import auth
from . import guidance

load_dotenv()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        DATABASE_URL=os.getenv('DATABASE_URL'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)


    from . import auth
    app.register_blueprint(auth.bp)

    from . import guidance
    app.register_blueprint(guidance.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app

def get_params():
    json_path = os.path.join(os.curdir, 'config', 'config.json')
    with open(json_path, 'r') as c:
        params = json.load(c)["params"]
    return params