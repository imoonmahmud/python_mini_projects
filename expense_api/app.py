from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timezone, timedelta

from models import db, User, Expense, Category
from validators import (
    login_required,
    validate_register,
    validate_create_expense,
    validate_update_expense
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


@app.route('/expenses/create', methods=['POST'])
@login_required
def create_expense(user):
    data = request.get_json()
    validate_create_expense(data)

    category = data.get('category', 'uncategorized')

    category_data = Category.query.filter_by(name=category).first()
    if not category_data:
        category_data = Category(name=category)
        db.session.add(category_data)
        db.session.commit()

    new_expense = Expense(
        title=data['title'],
        category_id = category_data.id,
        amount = data['amount'],
        user_id = int(user)
    )
    db.session.add(new_expense)
    db.session.commit()

    return {
        'message': 'Expense Created!',
        'data': {
            'id': new_expense.id,
            'title': new_expense.title,
            'amount': new_expense.amount,
            'created_at': new_expense.created_at,
            'owner': new_expense.user.username
        }
    }, 201


@app.route('/expenses/<int:id>', methods=['DELETE'])
@login_required
def delete_expense(user, id):
    data = Expense.query.filter_by(id=id, user_id=user).first()
    if not data:
        raise ValueError(f"Expense with expense_id '{id}' doesn't exists")

    db.session.delete(data)
    db.session.commit()
    return '', 204


@app.route('/expenses/<int:id>', methods=['PUT'])
@login_required
def update_expense(user, id):
    data = Expense.query.filter_by(id=id, user_id=user).first()
    if not data:
        raise ValueError(f"Expense with expense_id '{id}' doesn't exists")

    updated_expense = request.get_json()
    validate_update_expense(updated_expense)

    category_data = Category.query.filter_by(name=updated_expense['category']).first()
    if not category_data:
        category_data = Category(name=updated_expense['category'])
        db.session.add(category_data)
        db.session.commit()

    data.title = updated_expense['title']
    data.amount = updated_expense['amount']
    data.category_id = category_data.id
    db.session.commit()

    return {
        'message': 'Expense Updated',
        'data': {
            "id": data.id,
            "title": data.title,
            "amount": data.amount,
            "created_at": data.created_at,
            "owner": data.user.username
        }
    }, 200


@app.route('/expenses', methods=['GET'])
@login_required
def get_expenses(user):
    data = Expense.query.filter_by(user_id=user).all()
    expenses = []
    for expense in data:
        expenses.append({
            "id": expense.id,
            "title": expense.title,
            "amount": expense.amount,
            "created_at": expense.created_at,
        })
    return {'data': expenses}, 200



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)