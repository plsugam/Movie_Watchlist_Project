from flask import Flask, render_template
from app import config


def create_app():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY

    from app.routes import authRoutes
    app.register_blueprint(authRoutes.register())

    from app.routes import watchlistRoutes
    app.register_blueprint(watchlistRoutes.register())

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    return app
