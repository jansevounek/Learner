from flask import Flask
from flask_cors import CORS
from flask_supabase import Supabase

from .routes.teams import UserTeamRoutes, AdminTeamRoutes
from .routes.lessons import AdminLessonRoutes, UserLessonRoutes
from .routes import PaymentRoutes

supabase = Supabase()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Stripe routes
    app.register_blueprint(PaymentRoutes.bp)

    # Team routes
    app.register_blueprint(UserTeamRoutes.bp)
    app.register_blueprint(AdminTeamRoutes.bp)

    # Lesson routes
    app.register_blueprint(AdminLessonRoutes.bp)
    app.register_blueprint(UserLessonRoutes.bp)

    return app