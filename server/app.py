#!/usr/bin/env python3
import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from config import db, bcrypt
from resources import Signup, CheckSession, Login, Logout, RecipeIndex


def create_app(test_config=None):
    app = Flask(__name__, static_folder=None)

    # Config
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.json.compact = False

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)

    # API + Resources
    api = Api(app)
    api.add_resource(Signup, "/signup")
    api.add_resource(CheckSession, "/check_session")
    api.add_resource(Login, "/login")
    api.add_resource(Logout, "/logout")
    api.add_resource(RecipeIndex, "/recipes")

    @app.route('/')
    def index():
        return {"message": "API is running"}, 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5555)
