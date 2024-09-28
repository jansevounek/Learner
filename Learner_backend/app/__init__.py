from flask import Flask
from flask_cors import CORS
from flask_supabase import Supabase
import os
from .routes import ContainerRoutes, CreateContainerRoute, PaymentRoutes

supabase = Supabase()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Routes that delete or make containers
    app.register_blueprint(CreateContainerRoute.bp)

    # Other Container routes
    app.register_blueprint(ContainerRoutes.bp)

    # Payment routes
    app.register_blueprint(PaymentRoutes.bp)

    return app