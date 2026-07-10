import os
import pytest
from unittest.mock import patch, MagicMock
from werkzeug.security import generate_password_hash
from flask import Flask

from app.routes import authRoutes

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, "app", "templates")
STATIC_DIR = os.path.join(PROJECT_ROOT, "app", "static")


@pytest.fixture(scope="module")
def app():
    app = Flask(
        __name__,
        template_folder=TEMPLATE_DIR,
        static_folder=STATIC_DIR,
    )
    app.secret_key = "test-secret"
    app.config["TESTING"] = True
    app.register_blueprint(authRoutes.register())
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


# ── Login page ──────────────────────────────────────────────

def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_login_empty_fields(client):
    response = client.post("/login", data={"email": "", "password": ""})
    assert response.status_code == 200


@patch("app.controllers.authController.get_connection")
def test_login_success(mock_conn, client):
    fake_user = {
        "id": 1,
        "name": "Rana",
        "email": "rana@test.com",
        "password": generate_password_hash("password123"),
    }
    cursor = MagicMock()
    cursor.fetchone.return_value = fake_user
    conn = MagicMock()
    conn.cursor.return_value = cursor
    mock_conn.return_value = conn

    response = client.post(
        "/login",
        data={"email": "rana@test.com", "password": "password123"},
        follow_redirects=False,
    )
    assert response.status_code == 302

    with client.session_transaction() as sess:
        assert sess["user_id"] == 1
        assert sess["user_name"] == "Rana"


@patch("app.controllers.authController.get_connection")
def test_login_wrong_password(mock_conn, client):
    fake_user = {
        "id": 1,
        "name": "Rana",
        "email": "rana@test.com",
        "password": generate_password_hash("correctpassword"),
    }
    cursor = MagicMock()
    cursor.fetchone.return_value = fake_user
    conn = MagicMock()
    conn.cursor.return_value = cursor
    mock_conn.return_value = conn

    response = client.post(
        "/login",
        data={"email": "rana@test.com", "password": "wrongpassword"},
    )
    assert response.status_code == 200


@patch("app.controllers.authController.get_connection")
def test_login_user_not_found(mock_conn, client):
    cursor = MagicMock()
    cursor.fetchone.return_value = None
    conn = MagicMock()
    conn.cursor.return_value = cursor
    mock_conn.return_value = conn

    response = client.post(
        "/login",
        data={"email": "ghost@test.com", "password": "password123"},
    )
    assert response.status_code == 200


# ── Register page ────────────────────────────────────────────

def test_register_page_loads(client):
    response = client.get("/register")
    assert response.status_code == 200


def test_register_empty_fields(client):
    response = client.post(
        "/register",
        data={"name": "", "email": "", "password": ""},
    )
    assert response.status_code == 200


def test_register_short_password(client):
    response = client.post(
        "/register",
        data={"name": "Rana", "email": "rana@test.com", "password": "123"},
    )
    assert response.status_code == 200


@patch("app.controllers.authController.get_connection")
def test_register_email_already_exists(mock_conn, client):
    cursor = MagicMock()
    cursor.fetchone.return_value = {"id": 1, "email": "rana@test.com"}
    conn = MagicMock()
    conn.cursor.return_value = cursor
    mock_conn.return_value = conn

    response = client.post(
        "/register",
        data={"name": "Rana", "email": "rana@test.com", "password": "password123"},
        follow_redirects=False,
    )
    assert response.status_code == 302


@patch("app.controllers.authController.get_connection")
def test_register_success(mock_conn, client):
    cursor = MagicMock()
    cursor.fetchone.return_value = None  # email not taken
    conn = MagicMock()
    conn.cursor.return_value = cursor
    mock_conn.return_value = conn

    response = client.post(
        "/register",
        data={"name": "Rana", "email": "newuser@test.com", "password": "password123"},
        follow_redirects=False,
    )
    assert response.status_code == 302


# ── Logout ───────────────────────────────────────────────────

def test_logout_clears_session(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["user_name"] = "Rana"

    response = client.get("/logout", follow_redirects=False)
    assert response.status_code == 302

    with client.session_transaction() as sess:
        assert "user_id" not in sess
