from app import app
from models import db, User, Task
with app.app_context():
    tasks = Task.query.all()
    for task in tasks:
        print(task.id, task.title, task.done, task.created_at)