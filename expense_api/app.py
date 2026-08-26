from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timezone, timedelta



from models import db, User
from validators import (
    validate_register
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
SECRET_KEY = 'imoonmahmud'

def now_utc():
    return datetime.now(timezone.utc)


@app.route('/')
def home():
    return '<h1>Welcome to Expense Tracker API</h1>'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    validate_register(data)

    # check if the username already exists
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        raise ValueError(f"Username '{data['username']}' already exists")

    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return {'message': 'User created successfully!'}, 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    validate_register(data)

    user_data = User.query.filter_by(username=data['username']).first()
    if user_data and check_password_hash(user_data.password_hash, data['password']):
        token = jwt.encode(
            {
                'user': str(user_data.id),
                'exp': now_utc() + timedelta(hours=2)
            },
            SECRET_KEY,
            algorithm='HS256'
        )

        return {
            'message': 'Logged in successfully.',
            'token': token
        }
    raise ValueError('Invalid username or password.')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)