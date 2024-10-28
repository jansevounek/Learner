from flask import Flask
from flask_cors import CORS
from flask_supabase import Supabase
import os

from .routes.maindocker import CreateContainerRoute, DeleteContainerRoute
from .routes.teams import UserTeamRoutes, AdminTeamRoutes
from .routes.lessons import AdminLessonRoutes

supabase = Supabase()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Route that creates containers
    app.register_blueprint(CreateContainerRoute.bp)

    # Route that deletes containers
    app.register_blueprint(DeleteContainerRoute.bp)

    # Team routes
    app.register_blueprint(UserTeamRoutes.bp)
    app.register_blueprint(AdminTeamRoutes.bp)

    # Lesson routes
    app.register_blueprint(AdminLessonRoutes.bp)

    return app