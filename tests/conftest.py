import os
import pytest
from flask import Flask, Blueprint
from app.controllers import authController, watchlistController
from app.auth import login_required

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, "app", "templates")
STATIC_DIR = os.path.join(PROJECT_ROOT, "app", "static")


def make_auth_blueprint():
    bp = Blueprint("auth", __name__)
    bp.route("/login", methods=["GET", "POST"])(authController.login)
    bp.route("/register", methods=["GET", "POST"])(authController.register)
    bp.route("/", methods=["GET", "POST"])(login_required(authController.home))
    bp.route("/logout", methods=["GET", "POST"])(authController.logout)
    return bp


def make_watchlist_blueprint():
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
def full_app():
    """App with both auth and watchlist blueprints registered."""
    app = Flask(
        __name__,
        template_folder=TEMPLATE_DIR,
        static_folder=STATIC_DIR,
    )
    app.secret_key = "test-secret"
    app.config["TESTING"] = True
    app.register_blueprint(make_auth_blueprint())
    app.register_blueprint(make_watchlist_blueprint())
    return app
