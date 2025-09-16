# seed.py
from app import create_app
from models import db, User, Recipe

app = create_app()
app.app_context().push()

db.create_all()

# clear existing
Recipe.query.delete()
User.query.delete()
db.session.commit()

u1 = User(username="ava", image_url="https://example.com/ava.jpg", bio="I love cooking!")
u1.password = "password1"
u2 = User(username="omar", image_url="https://example.com/omar.jpg", bio="Baker and dev.")
u2.password = "password2"

db.session.add_all([u1, u2])
db.session.commit()

r1 = Recipe(
    title="Best pancakes",
    instructions=("Mix flour, milk, eggs, whisk well. Cook on medium heat turning once. " * 3)[:300],
    minutes_to_complete=20,
    user=u1
)
r2 = Recipe(
    title="Slow roasted chicken",
    instructions=("Season chicken, roast for 90 mins, baste occasionally. " * 3)[:250],
    minutes_to_complete=100,
    user=u2
)

db.session.add_all([r1, r2])
db.session.commit()

print("Seeded DB with users and recipes.")
