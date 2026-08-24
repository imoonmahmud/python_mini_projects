from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from models import db, User, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SECRET_KEY'] = 'imoonmahmud'
db.init_app(app)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # check if the email already have account
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('email already has an account')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created! Please log in.')
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/login', methods=['Get', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            flash('Logged in successfully.')
            return redirect(url_for('home'))
        else:
            flash('Invalid email and password.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out.')
    return redirect(url_for('home'))




def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.')
            return redirect(url_for(('login')))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/tasks')
@login_required
def tasks():
    user_tasks = Task.query.filter_by(user_id=session['user_id']).all()
    return render_template('tasks.html', tasks=user_tasks)

@app.route('/tasks/add', methods=['POST'])
@login_required
def add_task():
    title = request.form['title']
    if title.strip():
        new_task = Task(title=title, user_id=session['user_id'])
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/tasks/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != session['user_id']:
        flash("You can't modify that task.")
        return redirect(url_for('tasks'))
    task.done = not task.done
    db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != session['user_id']:
        flash("You can't edit that task.")
        return redirect(url_for('tasks'))

    if request.method == 'POST':
        task.title = request.form['title']
        db.session.commit()
        return redirect(url_for('tasks'))

    return render_template('edit_task.html', task=task)

@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != session['user_id']:
        flash("You can't delete that task.")
        return redirect(url_for('tasks'))
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    