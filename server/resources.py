from flask import request, session
from flask_restful import Resource
from models import db, User, Recipe

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:  # ✅ strict validation
            return {"error": "Invalid username or password"}, 422

        try:
            user = User(
                username=username,
                image_url=data.get("image_url", ""),
                bio=data.get("bio", "")
            )
            user.password_hash = password
            db.session.add(user)
            db.session.commit()
            session["user_id"] = user.id
            return user.to_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 422


class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")
        if user_id:
            user = User.query.get(user_id)
            return user.to_dict(), 200
        return {"error": "Unauthorized"}, 401


class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get("username")).first()
        if user and user.authenticate(data.get("password")):
            session["user_id"] = user.id
            return user.to_dict(), 200
        return {"error": "Invalid credentials"}, 401


class Logout(Resource):
    def delete(self):
        if "user_id" not in session:   # ✅ unauthorized check
            return {"error": "Unauthorized"}, 401
        session.pop("user_id", None)
        return {}, 204


class RecipeIndex(Resource):
    def get(self):
        if "user_id" not in session:   # ✅ unauthorized check
            return {"error": "Unauthorized"}, 401
        recipes = Recipe.query.all()
        return [recipe.to_dict() for recipe in recipes], 200

    def post(self):
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401

        data = request.get_json()
        if not data.get("title") or not data.get("instructions") or not data.get("minutes_to_complete"):
            return {"error": "Invalid recipe"}, 422

        try:
            recipe = Recipe(
                title=data["title"],
                instructions=data["instructions"],
                minutes_to_complete=data["minutes_to_complete"],
                user_id=user_id
            )
            db.session.add(recipe)
            db.session.commit()
            return recipe.to_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 422
