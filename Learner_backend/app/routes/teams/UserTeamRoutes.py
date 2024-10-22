from flask import Blueprint, jsonify, request

from ...services.supabase_service import supabase, getTeam, getUserExtra
from ...services.docker_service import docker

bp = Blueprint('user_teams', __name__, url_prefix='/teams/user')

@bp.route('/leave', methods=['POST'])
def leave_team():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    team = getTeam(name=json["team_name"])
    extra = getUserExtra(user_id=json["user_id"])

    if (extra):
        if (team):
            arr = extra[0].get("teams")

            for i in range(len(team)):
                arr.remove(team[i].get("id"))
            
            try:
                supabase.table("user").update({ "teams": arr }).eq("id", extra[0].get("id")).execute()
            except Exception as e:
                print(f"Error during Supabase query (during updating the user teams column): {e}")
                return "Error occured", 500
        else:
            return jsonify({
                "status": False,
                "msg": 'You are not a part of team "' + json["team_name"] + '"'
            })
    else:
        return jsonify({
                "status": False,
                "msg": 'Your user profile is incomplete - contact support'
            })

    return jsonify({
        "status": True,
        "msg": 'Successfully left team(s): "' + json["team_name"] + '"'
        })

@bp.route('/join', methods=['POST'])
def join_team():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    extra = getUserExtra(user_id=json["user_id"])
    team = getTeam(code=json["team_code"])

    if (extra):
        if (team):
            if extra[0].get("teams"):
                arr = extra[0].get("teams")
            else:
                arr = []

            if team[0].get("id") in arr:
                return jsonify({
                        "status": False,
                        "msg": 'You are already a part of team "' + team[0].get("name") + '"'
                    })
            
            arr.append(team[0].get("id"))

            try:
                supabase.table("user").update({ "teams": arr }).eq("id", extra[0].get("id")).execute()
            except Exception as e:
                print(f"Error during Supabase query (during updating the user teams column): {e}")
                return "Error occured", 500
        else:
            return jsonify({
                    "status": False,
                    "msg": 'No team with the code "' + json["team_code"] + '" found'
                })
    else:
        return jsonify({
                "status": False,
                "msg": 'Your user profile is incomplete - contact support'
            })

    return jsonify({
        "status": True,
        "msg": 'You successfully joined team "' + team[0].get("name") + '"'
        })