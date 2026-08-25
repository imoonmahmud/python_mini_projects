from werkzeug.security import check_password_hash
from app import app
from models import db, User
with app.app_context():
    users = User.query.all()
    for user in users:
        print(user.id, user.username)