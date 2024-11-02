from flask import Blueprint, jsonify, request

from ...services.supabase_service import supabase, getUserExtra, getUserLimitations, getLesson
from ...services.docker_service import docker

bp = Blueprint('user_lessons', __name__, url_prefix='/lessons/user')

@bp.route('/create-container', methods=['POST'])
def create_container():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})

    extra = getUserExtra(user_id=json["user_id"])

    print(extra)

    return jsonify({
        "status": True,
        "msg": 'on skibidi'
        })