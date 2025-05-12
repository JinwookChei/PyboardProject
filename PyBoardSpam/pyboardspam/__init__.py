from flask import Flask

def create_app():
    app = Flask(__name__)

    from . import spam
    app.register_blueprint(spam.bp)

    return app