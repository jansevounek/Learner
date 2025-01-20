from flask import Blueprint, jsonify, request

from ...services.supabase_service import supabase, getTeam, getUserExtra, getLesson
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
    lessons = getLesson(team_id=team[0].get("id"))

    if (extra and lessons):
        if (team):
            if extra[0].get("id") == team[0].get("creator_id"):
                return jsonify({
                    "status": False,
                    "msg": 'You cannot leave a team you have created'
                })
            else:
                for lesson in lessons:
                    try:
                        c = supabase.table("container").select("*").eq("user_id", extra[0].get("id")).eq("lesson_id", lesson.get("id")).execute()
                        container = c.data
                    except Exception as e:
                        print(f"Error during Supabase query (during gettin to be deleted containers): {e}")
                        return "Error occured", 500
                    
                    if len(container) == 1:

                        docker_container = docker.containers.get(container[0].get("name"))

                        if docker_container.status == "running":
                            docker_container.stop()
                        docker_container.remove()
                        
                        try:
                            supabase.table("container").delete().eq("id", container[0].get("id")).execute()
                        except Exception as e:
                            print(f"Error during Supabase query (during deleting a container): {e}")
                            return "Error occured", 500
                    elif len(container) > 1:
                        return jsonify({
                            "status": False,
                            "msg": 'There has been a problem processing your request - contact support'
                        })

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
            
            if team[0].get("member_count") >= team[0].get("member_limit"):
                return jsonify({
                        "status": False,
                        "msg": 'Team "' + team[0].get("name") + '" is already full'
                    })
            
            arr.append(team[0].get("id"))

            count = team[0].get("member_count")
            count += 1

            try:
                supabase.table("user").update({ "teams": arr }).eq("id", extra[0].get("id")).execute()
            except Exception as e:
                print(f"Error during Supabase query (during updating the user teams column): {e}")
                return "Error occured", 500
            
            try:
                supabase.table("team").update({ "member_count": count }).eq("team_code", json["team_code"]).execute()
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