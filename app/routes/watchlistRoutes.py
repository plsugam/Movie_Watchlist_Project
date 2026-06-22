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
    bp.route("/watchlist/edit/<int:id>", methods=["GET", "POST"])(
        login_required(watchlistController.edit_title)
    )
    bp.route("/watchlist/delete/<int:id>", methods=["GET", "POST"])(
        login_required(watchlistController.delete_title)
    )
    return bp
