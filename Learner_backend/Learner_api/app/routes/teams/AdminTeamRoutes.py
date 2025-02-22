from flask import Blueprint, jsonify, request

from ...services.supabase_service import supabase, getUserExtra, getUserLimitations, getTeam, getLesson
from ...services.docker_service import docker

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
    existing_team = getTeam(name=json["team_name"])

    if (extra and limit):
        if (not existing_team):
            if limit[0].get("team_limit") > limit[0].get("teams"):
                try:
                    t = supabase.table("team").insert({ "name": json["team_name"], "creator_id": extra[0].get("id") }).execute()
                    team = t.data
                except Exception as e:
                    print(f"Error during Supabase query (during inserting when creating new team): {e}")
                    return jsonify({
                        "status": False,
                        "msg": 'There has been a problem creating team: "' + json["team_name"] + '" - contact support'
                    })
                
                new_teams = extra[0].get("teams")
                new_teams.append(team[0].get("id"))

                try:
                    supabase.table("user").update({ "teams": new_teams }).eq("id", extra[0].get("id")).execute()
                except Exception as e:
                    print(f"Error during Supabase query (during updating user information on teams): {e}")
                    return jsonify({
                        "status": False,
                        "msg": 'There has been a problem creating team: "' + json["team_name"] + '" - contact support'
                    })

                try:
                    supabase.table("limitations").update({ "teams": limit[0].get("teams") + 1 }).eq("extra_id", extra[0].get("id")).execute()
                except Exception as e:
                    print(f"Error during Supabase query (during updating user limits - team creation): {e}")
                    return jsonify({
                        "status": False,
                        "msg": 'There has been a problem creating team: "' + json["team_name"] + '" - contact support'
                    })
            else:
                return jsonify({
                        "status": False,
                        "msg": 'You have reached the limit of teams you can create (2)'
                    })
        else:
            return jsonify({
                    "status": False,
                    "msg": 'A team with name "'+ json["team_name"] +'" already exists'
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
            lesson = getLesson(team_id=team[0].get("id"))

            for l in lesson:
                try:
                    containers = docker.containers.list(all=True)

                    for container in containers:
                        if container.name.startswith(l.get("name") + "-"):
                            if container.status == "running":
                                container.stop()
                            container.remove()
                except Exception as e:
                    print(f"Error during deleting containers - lesson cancel: {e}")
                    return jsonify({
                        "status": False,
                        "msg": 'There has been a problem deleting team: "' + json["team_name"] + '" - contact support'
                    })
            
            subtract_lessons = 2 - len(lesson)
            
            subtract_teams = 2 - len(team)

            try:
                supabase.table("limitations").update({ "teams": subtract_teams, "lessons": subtract_lessons }).eq("extra_id", extra[0].get("id")).execute()
            except Exception as e:
                print(f"Error during Supabase query (during updating user limits - team creation): {e}")
                return jsonify({
                    "status": False,
                    "msg": 'There has been a problem deleting team: "' + json["team_name"] + '" - contact support'
                })
            
            try:
                supabase.table("team").delete().eq("name", json["team_name"]).execute()
            except Exception as e:
                print(f"Error during Supabase query (during deletion of a team): {e}")
                return jsonify({
                    "status": False,
                    "msg": 'There has been a problem deleting team: "' + json["team_name"] + '" - contact support'
                })
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

@bp.route('/kick', methods=['POST'])
def kick_user():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    extra = getUserExtra(user_id=json["user_id"])

    if (extra):
        try:
            t = supabase.table("team").select("*").eq("name", json["team_name"]).eq("creator_id", extra[0].get("id")).execute()
            team = t.data
        except Exception as e:
            print(f"Error during Supabase query (during deletion of a team): {e}")
            return jsonify({
                "status": False,
                "msg": 'There has been a problem kicking user - contact support'
            })
        
        if (team):
            user = getUserExtra(code=json["user_code"])
            
            if (user):
                
                if user[0].get("id") == extra[0].get("id"):
                    return jsonify({
                        "status": False,
                        "msg": 'You cannot kick yourself out of a team you have created'
                    })
                
                newTeams = user[0].get("teams")
                newTeams.remove(team[0].get("id"))

                lessons = getLesson(team_id=team[0].get("id"))

                for lesson in lessons:
                    try:
                        c = supabase.table("container").select("*").eq("user_id", user[0].get("id")).eq("lesson_id", lesson.get("id")).execute()
                        container = c.data
                    except Exception as e:
                        print(f"Error during Supabase query (during gettin to be deleted containers): {e}")
                        return jsonify({
                            "status": False,
                            "msg": 'There has been a problem kicking user - contact support'
                        })
                    
                    if len(container) == 1:

                        docker_container = docker.containers.get(container[0].get("name"))

                        if docker_container.status == "running":
                            docker_container.stop()
                        docker_container.remove()
                        
                        try:
                            supabase.table("container").delete().eq("id", container[0].get("id")).execute()
                        except Exception as e:
                            print(f"Error during Supabase query (during deleting a container): {e}")
                            return jsonify({
                                "status": False,
                                "msg": 'There has been a problem kicking user - contact support'
                            })
                    elif len(container) > 1:
                        return jsonify({
                            "status": False,
                            "msg": 'There has been a problem processing your request - contact support'
                        })

                try:
                    supabase.table("user").update({"teams": newTeams}).eq("id", user[0].get("id")).execute()
                except Exception as e:
                    print(f"Error during Supabase query (during deletion of a team): {e}")
                    return jsonify({
                        "status": False,
                        "msg": 'There has been a problem kicking user - contact support'
                    })
                
                try:
                    supabase.table("team").update({ "member_count": team[0].get("member_count") - 1 }).eq("id", team[0].get("id")).execute()
                except Exception as e:
                    print(f"Error during Supabase query (during updating the team member_count column): {e}")
                    return jsonify({
                        "status": False,
                        "msg": 'There has been a problem kicking user - contact support'
                    })
            else:
                return jsonify({
                    "status": False,
                    "msg": 'No user with provided code found'
                })
        else:
            return jsonify({
                "status": False,
                "msg": 'No team with name "' + json["team_name"] + '" found'
            })
    else:
        return jsonify({
            "status": False,
            "msg": 'Your user profile is incomplete - contact support'
        })
    
    return jsonify({
            "status": True,
            "msg": 'You successfully kicked user with email "' + extra[0].get("email") + '"'
        })