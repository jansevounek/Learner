from flask import Blueprint, jsonify

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/', methods=['GET'])
def get_users():
    users = "test"
    return jsonify(users)