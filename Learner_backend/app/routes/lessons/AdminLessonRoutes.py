from flask import Blueprint, jsonify, request

from ...services.supabase_service import supabase, getUserExtra, getUserLimitations, getTeam
from ...services.docker_service import docker

bp = Blueprint('admin_lessons', __name__, url_prefix='/lessons/admin')

@bp.route('/create', methods=['POST'])
def create_lesson():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    print(json)

    return jsonify({
        "status": True,
        "msg": 'on skibidi'
        })