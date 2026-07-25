import os
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, Blueprint
from app.controllers import watchlistController
from app.auth import login_required

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, "app", "templates")
STATIC_DIR = os.path.join(PROJECT_ROOT, "app", "static")


def make_watchlist_blueprint():
    """Create a fresh watchlist blueprint for each test session."""
    bp = Blueprint("watchlist", __name__)
    bp.route("/dashboard", methods=["GET"])(
        login_required(watchlistController.dashboard)
    )
    bp.route("/watchlist", methods=["GET"])(
        login_required(watchlistController.view_watchlist)
    )
    bp.route("/watchlist/add", methods=["GET", "POST"])(
        login_required(watchlistController.add_title)
    )
    bp.route("/watchlist/edit/<int:id>", methods=["GET", "POST"])(
        login_required(watchlistController.edit_title)
    )
    bp.route("/watchlist/delete/<int:id>", methods=["GET", "POST"])(
        login_required(watchlistController.delete_title)
    )
    return bp


@pytest.fixture(scope="module")
def app():
    app = Flask(
        __name__,
        template_folder=TEMPLATE_DIR,
        static_folder=STATIC_DIR,
    )
    app.secret_key = "test-secret"
    app.config["TESTING"] = True
    app.register_blueprint(make_watchlist_blueprint())
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def logged_in_client(client):
    """Helper: puts a user in the session with a CSRF token."""
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["user_name"] = "Rana"
        sess["csrf_token"] = "test-token"
    return client


# ── Auth protection ──────────────────────────────────────────

def test_watchlist_redirects_guest(client):
    response = client.get("/watchlist", follow_redirects=False)
    assert response.status_code == 302


def test_dashboard_redirects_guest(client):
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 302


def test_add_redirects_guest(client):
    response = client.get("/watchlist/add", follow_redirects=False)
    assert response.status_code == 302


# ── Dashboard ────────────────────────────────────────────────

@patch("app.controllers.watchlistController.watchlist_repo")
def test_dashboard_loads(mock_repo, logged_in_client):
    mock_repo.get_count_by_user.return_value = 5
    mock_repo.get_status_counts.return_value = {}
    mock_repo.get_type_counts.return_value = {}
    mock_repo.get_recent.return_value = []

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
        data={"title": "", "type": "", "csrf_token": "test-token"},
    )
    assert response.status_code == 200


def test_add_title_invalid_type(logged_in_client):
    response = logged_in_client.post(
        "/watchlist/add",
        data={"title": "Inception", "type": "cartoon", "csrf_token": "test-token"},
    )
    assert response.status_code == 200


def test_add_title_invalid_year(logged_in_client):
    response = logged_in_client.post(
        "/watchlist/add",
        data={
            "title": "Inception",
            "type": "movie",
            "year": "1800",
            "csrf_token": "test-token",
        },
    )
    assert response.status_code == 200


def test_add_title_invalid_rating(logged_in_client):
    response = logged_in_client.post(
        "/watchlist/add",
        data={
            "title": "Inception",
            "type": "movie",
            "rating": "10",
            "csrf_token": "test-token",
        },
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
            "csrf_token": "test-token",
        },
        follow_redirects=False,
    )
    assert response.status_code == 302


# ── Edit title ───────────────────────────────────────────────

@patch("app.controllers.watchlistController.watchlist_repo")
def test_edit_title_not_found(mock_repo, logged_in_client):
    mock_repo.get_by_id.return_value = None

    response = logged_in_client.get(
        "/watchlist/edit/999", follow_redirects=False
    )
    assert response.status_code == 302


@patch("app.controllers.watchlistController.watchlist_repo")
def test_edit_title_page_loads(mock_repo, logged_in_client):
    fake_entry = {
        "id": 1, "user_id": 1, "title": "Inception",
        "type": "movie", "status": "completed",
        "genre": "Sci-Fi", "year": 2010, "rating": 5,
        "notes": "Great.", "poster_url": None,
    }
    mock_repo.get_by_id.return_value = fake_entry

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
        data={"csrf_token": "test-token"},
        follow_redirects=False,
    )
    assert response.status_code == 302
