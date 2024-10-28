from flask import Blueprint, jsonify, request

from ...services.supabase_service import supabase, getUserExtra, getUserLimitations, getTeam

bp = Blueprint('admin_teams', __name__, url_prefix='/teams/admin')

@bp.route('/create', methods=['POST'])
def create_team():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    extra = getUserExtra(user_id=json["user_id"])
    limit = getUserLimitations(user_id=json["user_id"])

    if (extra and limit):
        if limit[0].get("team_limit") > limit[0].get("teams"):
            try:
                supabase.table("team").insert({ "name": json["team_name"], "creator_id": extra[0].get("id") }).execute()
            except Exception as e:
                print(f"Error during Supabase query (during inserting when creating new team): {e}")
                return "Error occured", 500
            
            try:
                supabase.table("limitations").update({ "teams": limit[0].get("teams") + 1 }).eq("extra_id", extra[0].get("id")).execute()
            except Exception as e:
                print(f"Error during Supabase query (during updating user limits - team creation): {e}")
                return "Error occured", 500
        else:
            return jsonify({
                    "status": False,
                    "msg": 'You have reached the limit of teams you can create (2)'
                })
    else:
        return jsonify({
                "status": False,
                "msg": 'Your user profile is incomplete - contact support'
            })

    return jsonify({
        "status": True,
        "msg": 'You successfully created team "' + json["team_name"] + '"'
        })

@bp.route('/delete', methods=['POST'])
def delete_team():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    extra = getUserExtra(user_id=json["user_id"])
    team = getTeam(name=json["team_name"])

    if (extra):
        if (team):
            try:
                supabase.table("team").delete().eq("name", json["team_name"]).execute()
            except Exception as e:
                print(f"Error during Supabase query (during deletion of a team): {e}")
                return "Error occured", 500
            
            subtract = 2 - len(team)

            try:
                supabase.table("limitations").update({ "teams": subtract }).eq("extra_id", extra[0].get("id")).execute()
            except Exception as e:
                print(f"Error during Supabase query (during updating user limits - team creation): {e}")
                return "Error occured", 500
        else:
            return jsonify({
                    "status": False,
                    "msg": 'Team "' + json["team_name"] + '" does not exist'
                })
    else:
        return jsonify({
            "status": False,
            "msg": 'Your user profile is incomplete - contact support'
        })

    return jsonify({
            "status": True,
            "msg": 'You successfully deleted team(s) "' + json["team_name"] + '"'
        })