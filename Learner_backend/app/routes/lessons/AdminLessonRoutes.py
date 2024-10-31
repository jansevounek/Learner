from flask import Blueprint, jsonify, request

from ...services.supabase_service import supabase, getUserExtra, getUserLimitations, getLesson
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
    limit = getUserLimitations(user_id=json["user_id"])


    if (extra and limit):
        try:
            response = supabase.table("lesson").select("*").eq("name", json["name"]).eq("creator_id", extra[0].get("id")).execute()
        except Exception as e:
            print(f"Error during Supabase query (during checking for same lesson names): {e}")
            return "Error occured", 500
        if not response.data:
            if limit[0].get("lesson_limit") > limit[0].get("lessons"):
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

                try:
                    supabase.table("limitations").update({ "lessons": limit[0].get("lessons") + 1 }).eq("extra_id", extra[0].get("id")).execute()
                except Exception as e:
                    print(f"Error during Supabase query (during updating user limitations): {e}")
                    return "Error occured", 500
            else:
                return jsonify({
                    "status": False,
                    "msg": 'You have reached the maximum of lessons that you can create'
                })
        else:
            return jsonify({
                    "status": False,
                    "msg": 'You already have a lesson with the same name created'
                })
    else:
        return jsonify({
            "status": False,
            "msg": 'Your user profile is incomplete - contact support'
        })

    return jsonify({
        "status": True,
        "msg": 'on skibidi'
        })

# TODO unique names
@bp.route('/cancel', methods=['POST'])
def cancel_lesson():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    extra = getUserExtra(user_id=json["user_id"])
    limit = getUserLimitations(user_id=json["user_id"])
    lesson = getLesson(name=json["lesson_name"])

    if (extra and limit):
        if (lesson):
            try:
                supabase.table("lesson").delete().eq("name", json["lesson_name"]).eq("creator_id", extra[0].get("id")).execute()
            except Exception as e:
                print(f"Error during Supabase query (during creation of a lesson): {e}")
                return "Error occured", 500

            try:
                supabase.table("limitations").update({ "lessons": limit[0].get("lessons") - 1 }).eq("extra_id", extra[0].get("id")).execute()
            except Exception as e:
                print(f"Error during Supabase query (during creation of a lesson): {e}")
                return "Error occured", 500
        else:
            return jsonify({
                "status": False,
                "msg": 'No lesson with the name "' + json["lesson_name"] + '" found'
            })
    else:
        return jsonify({
            "status": False,
            "msg": 'Your user profile is incomplete - contact support'
        })
    
    return jsonify({
        "status": True,
        "msg": 'Lesson "' + json["lesson_name"] + '" canceled successfully'
        })