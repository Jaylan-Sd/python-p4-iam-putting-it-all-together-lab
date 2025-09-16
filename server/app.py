from flask import Flask, session, request, jsonify
from flask_migrate import Migrate
from models import db, User, Recipe

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'super-secret-key'

    db.init_app(app)   # ✅ attach db to app
    migrate = Migrate(app, db)

    # Example route
    @app.route('/')
    def index():
        return "App is running"

    return app

# If running directly (not just in tests)
app = create_app()
