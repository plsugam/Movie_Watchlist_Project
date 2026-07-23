# Reellog

A personal movie, series, and anime watchlist web application built with Flask, MySQL, and Jinja2.

---

## Table of Contents

- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Architecture](#architecture)
- [Database Design](#database-design)
- [Security](#security)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Version Control](#version-control)

---

## Overview

Reellog is a full-stack web application that allows users to track everything they watch. Users can register, log in, and maintain a personal watchlist of movies, series, and anime — complete with status tracking, ratings, genres, and personal notes.

The project was built as a semester final project for the module **ST5041CMD — The Internet and Web Technologies** at Softwarica College of IT & E-Commerce in collaboration with Coventry University.

---

## Technologies Used

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Templating | Jinja2 |
| Database | MySQL |
| Frontend | HTML, CSS, JavaScript |
| Authentication | Werkzeug (password hashing), Flask sessions |
| Security | CSRF token protection, input validation |
| Testing | pytest, unittest.mock |
| Version Control | Git, GitHub |
| Environment | python-dotenv |

---

## Features

- User registration and login with hashed passwords
- Session-based authentication with login required protection
- Personal watchlist — each user only sees their own titles
- Add, view, edit, and delete watchlist entries (full CRUD)
- Track watch status: Watching, Completed, Plan to Watch, Dropped
- Filter watchlist by type, status, and sort order
- Search titles by name
- Dashboard with stats — total titles, counts by status and type, recently added
- CSRF protection on all POST forms
- Client-side form validation with real-time feedback
- Custom error pages (403, 404, 500)
- Responsive design

---

## Architecture

The project follows an MVC-like pattern consistent with how Flask applications are structured in this module:

```
Reellog/
├── run.py                          # Entry point
├── requirements.txt
├── .env                            # Environment variables (not committed)
├── .gitignore
└── app/
    ├── __init__.py                 # App factory, CSRF hook, error handlers
    ├── config.py                   # Loads config from .env
    ├── database.py                 # MySQL connection, table creation
    ├── auth.py                     # login_required decorator
    ├── controllers/
    │   ├── authController.py       # Login, register, logout logic
    │   └── watchlistController.py  # Watchlist CRUD logic
    ├── repository/
    │   ├── user_repo.py            # Reusable user DB queries
    │   └── watchlist_repo.py       # Reusable watchlist DB queries
    ├── routes/
    │   ├── authRoutes.py           # Auth URL blueprint
    │   └── watchlistRoutes.py      # Watchlist URL blueprint
    ├── templates/
    │   ├── base.html               # Shared layout
    │   ├── login.html
    │   ├── register.html
    │   ├── dashboard.html
    │   ├── watchlist.html
    │   ├── add.html
    │   ├── edit.html
    │   └── errors/
    │       ├── 403.html
    │       ├── 404.html
    │       └── 500.html
    └── static/
        ├── css/
        │   ├── style.css
        │   ├── validation.css
        │   └── nav.css
        └── js/
            ├── carousel.js
            ├── watchlist.js
            └── validation.js
```

---

## Database Design

Two tables are used:

### `users`
| Column | Type | Description |
|---|---|---|
| id | INT AUTO_INCREMENT | Primary key |
| name | VARCHAR(100) | Display name |
| email | VARCHAR(100) UNIQUE | Login email |
| password | VARCHAR(255) | Bcrypt hashed password |
| role | VARCHAR(20) | 'user' or 'admin', defaults to 'user' |
| created_at | TIMESTAMP | Account creation time |

### `watchlist`
| Column | Type | Description |
|---|---|---|
| id | INT AUTO_INCREMENT | Primary key |
| user_id | INT | Foreign key → users.id |
| title | VARCHAR(200) | Title name |
| type | VARCHAR(20) | 'movie', 'series', or 'anime' |
| status | VARCHAR(30) | 'watching', 'completed', 'plan', or 'dropped' |
| genre | VARCHAR(50) | Optional genre |
| year | INT | Optional release year |
| rating | INT | Optional rating 1–5 |
| notes | TEXT | Optional personal notes |
| created_at | TIMESTAMP | Date added |

The `user_id` foreign key uses `ON DELETE CASCADE` — if a user is deleted, all their watchlist entries are automatically removed.

---

## Security

- **Password hashing** — all passwords are hashed using Werkzeug's `generate_password_hash` before being stored. Plain text passwords are never saved.
- **CSRF protection** — a random token (`os.urandom(16).hex()`) is generated per session and validated on every POST request via a `before_request` hook. Requests without a valid token are rejected with a 403 response.
- **Session management** — user identity and role are stored server-side in Flask's signed session cookie.
- **Input validation** — all form inputs are validated both client-side (JavaScript) and server-side (Python). Type and status fields use whitelist validation.
- **Parameterized queries** — all database queries use parameterized statements (`%s`) to prevent SQL injection.
- **User isolation** — all watchlist queries filter by `user_id`, preventing users from accessing or modifying each other's data.
- **Environment variables** — database credentials and secret key are stored in a `.env` file and never committed to version control.

---

## Setup and Installation

### Prerequisites
- Python 3.10+
- MySQL Server
- Git

### Steps

1. Clone the repository:
```bash
git clone https://github.com/plsugam/Movie_Watchlist_Project.git
cd Movie_Watchlist_Project
```

2. Install dependencies:
```bash
python -m pip install -r requirements.txt
```

3. Create a `.env` file in the root folder:
```
SECRET_KEY=your-secret-key-here
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your-password
MYSQL_DATABASE=watchlist_db
```

4. Create the database in MySQL:
```sql
CREATE DATABASE watchlist_db;
```

5. Run the application — tables are created automatically on first run:
```bash
python -m run
```

---

## Running the Application

```bash
python -m run
```

The app runs at `http://127.0.0.1:5000` by default.

---

## Running Tests

```bash
python -m pytest tests/ -v
```

Tests use `unittest.mock` to mock the database connection — no live MySQL connection is needed to run the test suite.

---

## Version Control

This project was version controlled from the beginning using Git. The repository is hosted at:

**GitHub:** https://github.com/plsugam/Movie_Watchlist_Project

**Demo Video:** *(link to be added after recording)*

Commits were made incrementally throughout development, with each logical change committed separately to demonstrate continuous progress.
