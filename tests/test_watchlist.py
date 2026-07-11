import os
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask

from app.routes import authRoutes
from app.routes import watchlistRoutes

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
    app.register_blueprint(watchlistRoutes.register())
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def logged_in_client(client):
    """Helper: puts a user in the session."""
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["user_name"] = "Rana"
    return client


# ── Auth protection ──────────────────────────────────────────

def test_watchlist_redirects_guest(client):
    response = client.get("/watchlist", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.location


def test_dashboard_redirects_guest(client):
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.location


def test_add_redirects_guest(client):
    response = client.get("/watchlist/add", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.location


# ── Dashboard ────────────────────────────────────────────────

@patch("app.controllers.watchlistController.get_connection")
def test_dashboard_loads(mock_conn, logged_in_client):
    cursor = MagicMock()
    cursor.fetchone.return_value = {"total": 5}
    cursor.fetchall.return_value = []
    conn = MagicMock()
    conn.cursor.return_value = cursor
    mock_conn.return_value = conn

    response = logged_in_client.get("/dashboard")
    assert response.status_code == 200


# ── View watchlist ───────────────────────────────────────────

@patch("app.controllers.watchlistController.get_connection")
def test_view_watchlist_loads(mock_conn, logged_in_client):
    cursor = MagicMock()
    cursor.fetchall.return_value = []
    conn = MagicMock()
    conn.cursor.return_value = cursor
    mock_conn.return_value = conn

    response = logged_in_client.get("/watchlist")
    assert response.status_code == 200


# ── Add title ────────────────────────────────────────────────

def test_add_title_page_loads(logged_in_client):
    response = logged_in_client.get("/watchlist/add")
    assert response.status_code == 200


def test_add_title_missing_fields(logged_in_client):
    response = logged_in_client.post(
        "/watchlist/add",
        data={"title": "", "type": ""},
    )
    assert response.status_code == 200


def test_add_title_invalid_type(logged_in_client):
    response = logged_in_client.post(
        "/watchlist/add",
        data={"title": "Inception", "type": "cartoon"},
    )
    assert response.status_code == 200


def test_add_title_invalid_year(logged_in_client):
    response = logged_in_client.post(
        "/watchlist/add",
        data={"title": "Inception", "type": "movie", "year": "1800"},
    )
    assert response.status_code == 200


def test_add_title_invalid_rating(logged_in_client):
    response = logged_in_client.post(
        "/watchlist/add",
        data={"title": "Inception", "type": "movie", "rating": "10"},
    )
    assert response.status_code == 200


@patch("app.controllers.watchlistController.get_connection")
def test_add_title_success(mock_conn, logged_in_client):
    cursor = MagicMock()
    conn = MagicMock()
    conn.cursor.return_value = cursor
    mock_conn.return_value = conn

    response = logged_in_client.post(
        "/watchlist/add",
        data={
            "title": "Inception",
            "type": "movie",
            "status": "completed",
            "genre": "Sci-Fi",
            "year": "2010",
            "rating": "5",
            "notes": "Great film.",
        },
        follow_redirects=False,
    )
    assert response.status_code == 302


# ── Edit title ───────────────────────────────────────────────

@patch("app.controllers.watchlistController.get_connection")
def test_edit_title_not_found(mock_conn, logged_in_client):
    cursor = MagicMock()
    cursor.fetchone.return_value = None
    conn = MagicMock()
    conn.cursor.return_value = cursor
    mock_conn.return_value = conn

    response = logged_in_client.get("/watchlist/edit/999", follow_redirects=False)
    assert response.status_code == 302


@patch("app.controllers.watchlistController.get_connection")
def test_edit_title_page_loads(mock_conn, logged_in_client):
    fake_entry = {
        "id": 1, "user_id": 1, "title": "Inception",
        "type": "movie", "status": "completed",
        "genre": "Sci-Fi", "year": 2010, "rating": 5, "notes": "Great."
    }
    cursor = MagicMock()
    cursor.fetchone.return_value = fake_entry
    conn = MagicMock()
    conn.cursor.return_value = cursor
    mock_conn.return_value = conn

    response = logged_in_client.get("/watchlist/edit/1")
    assert response.status_code == 200


# ── Delete title ─────────────────────────────────────────────

@patch("app.controllers.watchlistController.get_connection")
def test_delete_title(mock_conn, logged_in_client):
    cursor = MagicMock()
    conn = MagicMock()
    conn.cursor.return_value = cursor
    mock_conn.return_value = conn

    response = logged_in_client.post(
        "/watchlist/delete/1",
        follow_redirects=False,
    )
    assert response.status_code == 302
