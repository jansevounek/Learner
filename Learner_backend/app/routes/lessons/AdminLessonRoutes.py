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
    
    extra = getUserExtra(user_id=json["user_id"])

    if (extra):
        data = {
            "creator_id": extra[0].get("id"),
            "start_time": json["date"][0],
            "end_time": json["date"][1],
            "task": json["task"],
            "name": json["name"],
            "team_id": json["team_id"],
            "settings": json["container_settings"]
        }
        try:
            supabase.table("lesson").insert(data).execute()
        except Exception as e:
            print(f"Error during Supabase query (during creation of a lesson): {e}")
            return "Error occured", 500
    else:
        return jsonify({
            "status": False,
            "msg": 'Your user profile is incomplete - contact support'
        })

    return jsonify({
        "status": True,
        "msg": 'on skibidi'
        })