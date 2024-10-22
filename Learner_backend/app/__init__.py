from flask import Flask
from flask_cors import CORS
from flask_supabase import Supabase
import os

from .routes.maindocker import CreateContainerRoute, DeleteContainerRoute
from .routes.teams import UserTeamRoutes, AdminTeamRoutes
from .routes import ContainerRoutes, PaymentRoutes

supabase = Supabase()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Route that creates containers
    app.register_blueprint(CreateContainerRoute.bp)

    # Route that deletes containers
    app.register_blueprint(DeleteContainerRoute.bp)

    # Other Container routes
    app.register_blueprint(ContainerRoutes.bp)

    # Payment routes
    app.register_blueprint(PaymentRoutes.bp)

    # Team routes
    app.register_blueprint(UserTeamRoutes.bp)

    # Team routes
    app.register_blueprint(AdminTeamRoutes.bp)

    return app