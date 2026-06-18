from flask import Flask
from app import config
 
 
def create_app():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY
 
    from app.routes import authRoutes
    app.register_blueprint(authRoutes.register())
 
    return app