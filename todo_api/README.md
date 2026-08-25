# To-Do List API

A simple RESTful API for managing users' to-do lists, built with Flask and SQLite.

## Features

* User signup and login
* Secure password hashing
* Session-based authentication
* Create, edit, delete, and complete tasks
* User-specific tasks
* CSRF protection
* Custom 404 and 500 error pages

## Tech Stack

* Python
* Flask
* Flask-SQLAlchemy
* SQLite
* Flask-WTF

## Project Structure

```text
project/
├── app.py
├── models.py
├── templates/
└── todo.db
```

## Run Locally

Install the dependencies:

```bash
pip install flask flask-sqlalchemy flask-wtf
```

Run the application:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Main Routes

| Method   | Route                | Description                |
| -------- | -------------------- | -------------------------- |
| GET/POST | `/signup`            | Create an account          |
| GET/POST | `/login`             | Log in                     |
| GET      | `/logout`            | Log out                    |
| GET      | `/tasks`             | View your tasks            |
| POST     | `/tasks/add`         | Add a task                 |
| POST     | `/tasks/<id>/toggle` | Complete/uncomplete a task |
| GET/POST | `/tasks/<id>/edit`   | Edit a task                |
| POST     | `/tasks/<id>/delete` | Delete a task              |
