# Blogging Platform API

A simple RESTful API for managing blog posts, built with **Flask**, **Flask-RESTful**, **SQLAlchemy**, and **SQLite**.

## Features

* Create, read, update, and delete blog posts
* Search posts by title, content, or category
* SQLite database
* RESTful API endpoints
* No authentication or authorization required

## Tech Stack

* Python
* Flask
* Flask-RESTful
* Flask-SQLAlchemy
* SQLite

## API Endpoints

| Method | Endpoint           | Description       |
| ------ | ------------------ | ----------------- |
| GET    | `/posts`           | Get all posts     |
| GET    | `/posts?term=tech` | Search posts      |
| POST   | `/posts`           | Create a post     |
| GET    | `/posts/<id>`      | Get a single post |
| PATCH  | `/posts/<id>`      | Update a post     |
| DELETE | `/posts/<id>`      | Delete a post     |

### Search

Search posts using the `term` query parameter:

```text
GET /posts?term=tech
```

The search checks the `title`, `content`, and `category` fields.

## Example Post

```json
{
  "title": "Learning Python",
  "content": "Python is a powerful programming language.",
  "category": "Programming",
  "tags": ["python", "programming"]
}
```

## Acknowledgements

Core project idea from [roadmap.sh](https://roadmap.sh/projects/blogging-platform-api).