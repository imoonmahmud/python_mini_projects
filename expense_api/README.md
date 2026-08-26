# Expense Tracker API

A simple RESTful API for managing personal expenses, built with **Flask**, **SQLite**, **SQLAlchemy**, and **JWT authentication**.

## Features

* User registration and login
* Secure password hashing
* JWT-based authentication
* Create, read, update, and delete expenses
* Expense categories
* User-specific expense access
* Input validation
* SQLite database

## Tech Stack

* Python
* Flask
* Flask-SQLAlchemy
* SQLite
* PyJWT
* Werkzeug

## API Endpoints

| Method   | Endpoint           | Description            | Auth |
| -------- | ------------------ | ---------------------- | ---- |
| `GET`    | `/`                | Check API status       | No   |
| `POST`   | `/register`        | Create a new user      | No   |
| `POST`   | `/login`           | Log in and receive JWT | No   |
| `POST`   | `/expenses/create` | Create an expense      | Yes  |
| `GET`    | `/expenses`        | Get user's expenses    | Yes  |
| `PUT`    | `/expenses/<id>`   | Update an expense      | Yes  |
| `DELETE` | `/expenses/<id>`   | Delete an expense      | Yes  |

The application uses SQLite through SQLAlchemy and creates the database when the application starts.

## Project Structure

```text
project/
│
├── app.py
├── models.py
├── validators.py
├── database.db
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <project-folder>
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install flask flask-sqlalchemy pyjwt werkzeug
```

### 4. Run the application

```bash
python app.py
```

The API will run in Flask debug mode.

## Authentication

Register a user:

```http
POST /register
Content-Type: application/json
```

```json
{
  "username": "emon",
  "password": "password123"
}
```

Log in:

```http
POST /login
Content-Type: application/json
```

```json
{
  "username": "emon",
  "password": "password123"
}
```

A successful login returns a JWT token that is required for protected expense endpoints. The token expires after **2 hours**.

## Expense Example

Create an expense:

```http
POST /expenses/create
Authorization: Bearer <your-token>
Content-Type: application/json
```

```json
{
  "title": "Lunch",
  "amount": 250,
  "category": "Food"
}
```

The API automatically creates a category if it does not already exist.

## Get Expenses

```http
GET /expenses
Authorization: Bearer <your-token>
```

Returns the authenticated user's expenses.

```json
{
  "data": [
    {
      "id": 1,
      "title": "Lunch",
      "amount": 250,
      "created_at": "... "
    }
  ]
}
```

The endpoint filters expenses by the authenticated user's ID.

## Update an Expense

```http
PUT /expenses/1
Authorization: Bearer <your-token>
Content-Type: application/json
```

```json
{
  "title": "Dinner",
  "amount": 350,
  "category": "Food"
}
```

## Delete an Expense

```http
DELETE /expenses/1
Authorization: Bearer <your-token>
```

A successful deletion returns:

```http
204 No Content
```

## Security

* Passwords are stored using Werkzeug password hashing rather than plain text.
* Protected routes require authentication.
* Users can only access their own expenses.
* JWT tokens have a limited lifetime.

Password hashing is implemented during registration, while password verification is performed during login.
