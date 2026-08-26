from werkzeug.security import check_password_hash
from app import app
from models import db, User, Expense, Category
with app.app_context():
    expenses = Expense.query.all()
    for expense in expenses:
        print(expense.id, expense.category)


with app.app_context():
    categories = Category.query.all()
    for cat in categories:
        print(cat.id, cat.name)
