from flask import Blueprint
from app.controllers import authController
from app.auth import login_required

bp = Blueprint("auth", __name__)


def register():
    bp.route("/login", methods=["GET", "POST"])(
        authController.login
    )
    bp.route("/register", methods=["GET", "POST"])(
        authController.register
    )
    bp.route("/", methods=["GET", "POST"])(
        login_required(authController.home)
    )
    bp.route("/logout", methods=["GET", "POST"])(
        authController.logout
    )
    return bp
