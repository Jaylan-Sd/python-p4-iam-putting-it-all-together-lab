from flask import Flask, session, request, jsonify
from flask_migrate import Migrate
from models import db, User, Recipe

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'super-secret-key'

    db.init_app(app)
    migrate = Migrate(app, db)

    # ----------------------
    # INDEX
    # ----------------------
    @app.route('/')
    def index():
        return "App is running"

    # ----------------------
    # SIGNUP
    # ----------------------
    @app.route('/signup', methods=['POST'])
    def signup():
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password required"}), 422

        # check if username already exists
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already taken"}), 422

        # create user
        user = User(username=username)
        user.password_hash = password  # setter will hash it
        db.session.add(user)
        db.session.commit()

        # log them in (store session)
        session["user_id"] = user.id

        return jsonify({
            "id": user.id,
            "username": user.username,
            "image_url": user.image_url,
            "bio": user.bio
        }), 201  # ✅ created

    # ----------------------
    # LOGIN
    # ----------------------
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.authenticate(password):
            session["user_id"] = user.id
            return jsonify({"message": "Login successful"}), 200

        return jsonify({"error": "Invalid username or password"}), 401

    # ----------------------
    # LOGOUT
    # ----------------------
    @app.route('/logout', methods=['DELETE'])
    def logout():
        if "user_id" not in session or session["user_id"] is None:
            return jsonify({"error": "Not logged in"}), 401

        session.pop("user_id", None)
        return "", 204

    # ----------------------
    # RECIPES
    # ----------------------
    @app.route('/recipes', methods=['GET'])
    def get_recipes():
        if "user_id" not in session or session["user_id"] is None:
            return jsonify({"error": "Unauthorized"}), 401

        recipes = Recipe.query.all()
        return jsonify([
            {
                "id": r.id,
                "title": r.title,
                "instructions": r.instructions,
                "minutes_to_complete": r.minutes_to_complete,
                "user_id": r.user_id
            } for r in recipes
        ]), 200

    @
