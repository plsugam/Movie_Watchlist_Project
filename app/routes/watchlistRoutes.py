from flask import Blueprint
from app.controllers import watchlistController
from app.auth import login_required

bp = Blueprint("watchlist", __name__)


def register():
    bp.route("/watchlist", methods=["GET"])(
        login_required(watchlistController.view_watchlist)
    )
    bp.route("/watchlist/add", methods=["GET", "POST"])(
        login_required(watchlistController.add_title)
    )
    return bp
