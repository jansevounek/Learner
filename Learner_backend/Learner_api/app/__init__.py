from flask import Flask
from flask_cors import CORS
from flask_supabase import Supabase
import os

supabase = Supabase()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # supabase setup
    app.config['SUPABASE_URL'] = os.getenv('VITE_SUPABASE_URL')
    app.config['SUPABASE_KEY'] = os.getenv('VITE_SUPABASE_KEY')

    supabase.init_app(app)

    # dont move - done because of supabase
    from .routes import ContainerPhysicalRoutes, ContainerUserRoutes, PaymentRoutes

    # Routes that delete or make containers
    app.register_blueprint(ContainerPhysicalRoutes.bp)

    # Other Container routes
    app.register_blueprint(ContainerUserRoutes.bp)

    # Payment routes
    app.register_blueprint(PaymentRoutes.bp)

    return app