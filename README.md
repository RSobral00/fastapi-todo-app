# FastAPI Todo App

A full-stack todo application with user accounts, JWT authentication and role-based access, built with **FastAPI**, **SQLAlchemy** and **Jinja2** templates.

Users can register, log in, and create, edit, complete and delete their own todos. Admins can see and delete every user's todos.

> Built while taking [FastAPI – The Complete Course](https://www.udemy.com/course/fastapi-the-complete-course/) by Eric Roby, then extended on my own.

## Features

- **REST API** for todos, users and admin actions, with interactive docs at `/docs`
- **JWT authentication** (OAuth2 password flow) with bcrypt-hashed passwords
- **Role-based access**: admin-only endpoints
- **Per-user data isolation**: every query is filtered by owner, so users can only reach their own todos
- **Server-rendered pages** with Jinja2 and Bootstrap: login, register, todo list, add and edit
- **Database migrations** with Alembic
- **Test suite** with pytest, using a separate test database and dependency overrides
- **Secrets kept out of the code**: `SECRET_KEY` is loaded from a git-ignored `.env` file

## Tech stack

| Layer | Tools |
|---|---|
| Backend | FastAPI, Uvicorn, Pydantic |
| Database | SQLite, SQLAlchemy 2.0, Alembic |
| Auth | python-jose (JWT), passlib + bcrypt |
| Frontend | Jinja2, Bootstrap 4, vanilla JavaScript |
| Testing | pytest, pytest-asyncio, FastAPI TestClient |

## Getting started

Requires Python 3.10+.

```bash
git clone https://github.com/RSobral00/fastapi-todo-app.git
cd fastapi-todo-app

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Put a real key in .env. Generate one with:
openssl rand -hex 32

uvicorn TodoApp.main:app --reload
```

Open http://127.0.0.1:8000. You'll be sent to the login page; click **Register?** to create an account.

New accounts always get the `user` role; the API ignores any role sent by the client. To try the admin endpoints locally, promote your account in the database:

```bash
sqlite3 todosapp.db "UPDATE users SET role = 'admin' WHERE username = 'your-username';"
```

Then log in again so your new token carries the admin role.

The API docs are at http://127.0.0.1:8000/docs.

## Running the tests

```bash
pytest
```

## API overview

| Method | Path | Description | Auth |
|---|---|---|---|
| POST | `/auth/` | Register a user | – |
| POST | `/auth/token` | Log in, returns a JWT | – |
| GET | `/todos/` | List your todos | User |
| GET | `/todos/todo/{id}` | Get one of your todos | User |
| POST | `/todos/todo` | Create a todo | User |
| PUT | `/todos/todo/{id}` | Update a todo | User |
| DELETE | `/todos/todo/{id}` | Delete a todo | User |
| GET | `/user/` | Get your profile | User |
| PUT | `/user/password` | Change your password | User |
| PUT | `/user/phone_number/{number}` | Change your phone number | User |
| GET | `/admin/todo` | List all users' todos | Admin |
| DELETE | `/admin/todo/{id}` | Delete any todo | Admin |

## Project structure

```
TodoApp/
├── main.py          # app setup, static files, router registration
├── database.py      # SQLAlchemy engine and session
├── models.py        # Users and Todos tables
├── routers/         # auth, todos, users, admin (API endpoints + page routes)
├── templates/       # Jinja2 pages
├── static/          # CSS and JavaScript (Bootstrap + base.js)
├── alembic/         # database migrations
└── test/            # pytest suite
```
