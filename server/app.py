from flask import Flask, request, session, jsonify
from flask_migrate import Migrate
from models import db, User, Recipe

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "super-secret"  # needed for sessions

db.init_app(app)
migrate = Migrate(app, db)


# ----------------- Signup -----------------
@app.post("/signup")
def signup():
    data = request.get_json()
    try:
        new_user = User(
            username=data["username"],
            bio=data.get("bio"),
            image_url=data.get("image_url"),
        )
        new_user.password_hash = data["password"]

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id

        return jsonify({
            "id": new_user.id,
            "username": new_user.username,
            "bio": new_user.bio,
            "image_url": new_user.image_url,
        }), 201
    except Exception:
        return {"error": "Invalid user"}, 422


# ----------------- Check Session -----------------
@app.get("/check_session")
def check_session():
    user_id = session.get("user_id")
    if not user_id:
        return {"error": "Unauthorized"}, 401

    user = db.session.get(User, user_id)   # ✅ new way, not User.query.get
    if not user:
        return {"error": "Unauthorized"}, 401

    return jsonify({
        "id": user.id,
        "username": user.username,
        "bio": user.bio,
        "image_url": user.image_url,
    }), 200


# ----------------- Login -----------------
@app.post("/login")
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()

    if user and user.authenticate(data["password"]):
        session["user_id"] = user.id
        return jsonify({
            "id": user.id,
            "username": user.username,
            "bio": user.bio,
            "image_url": user.image_url,
        }), 200

    return {"error": "Invalid credentials"}, 401


# ----------------- Logout -----------------
@app.delete("/logout")
def logout():
    if not session.get("user_id"):
        return {"error": "Unauthorized"}, 401

    session.pop("user_id", None)   # ✅ better than setting None
    return {}, 204


# ----------------- Recipes -----------------
@app.get("/recipes")
def get_recipes():
    user_id = session.get("user_id")
    if not user_id:
        return {"error": "Unauthorized"}, 401

    user = db.session.get(User, user_id)   # ✅ new way
    return jsonify([
        {
            "id": recipe.id,
            "title": recipe.title,
            "instructions": recipe.instructions,
            "minutes_to_complete": recipe.minutes_to_complete,
        }
        for recipe in user.recipes
    ]), 200


@app.post("/recipes")
def create_recipe():
    user_id = session.get("user_id")
    if not user_id:
        return {"error": "Unauthorized"}, 401

    data = request.get_json()
    try:
        recipe = Recipe(
            title=data["title"],
            instructions=data["instructions"],
            minutes_to_complete=data["minutes_to_complete"],
            user_id=user_id,
        )
        db.session.add(recipe)
        db.session.commit()

        return jsonify({
            "id": recipe.id,
            "title": recipe.title,
            "instructions": recipe.instructions,
            "minutes_to_complete": recipe.minutes_to_complete,
        }), 201
    except Exception:
        return {"error": "Invalid recipe"}, 422


if __name__ == "__main__":
    app.run(port=5555, debug=True)
