import os
import subprocess
from flask import Blueprint, jsonify, request

from ...services.supabase_service import getScript, supabase, getUserExtra, getUserLimitations, getLesson, getContainer
from ...services.docker_service import docker

from datetime import datetime

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
            response = supabase.table("lesson").select("*").eq("name", json["name"]).execute()
        except Exception as e:
            print(f"Error during Supabase query (during checking for same lesson names): {e}")
            return jsonify({
                "status": False,
                "msg": 'There has been a problem creating your lesson - contact support'
            })
        if not response.data:
            if datetime.strptime(json["date"][1], "%Y-%m-%dT%H:%M:%S.%fZ") > datetime.now():
                if limit[0].get("lesson_limit") > limit[0].get("lessons"):
                    data = {
                        "creator_id": extra[0].get("id"),
                        "start_time": json["date"][0],
                        "end_time": json["date"][1],
                        "task": json["task"],
                        "name": json["name"],
                        "team_id": json["team_id"],
                        "settings": json["container_settings"],
                        "packages": json["pckg"]
                    }
                    try:
                        supabase.table("lesson").insert(data).execute()
                    except Exception as e:
                        print(f"Error during Supabase query (during creation of a lesson): {e}")
                        return jsonify({
                            "status": False,
                            "msg": 'There has been a problem creating your lesson - contact support'
                        })

                    try:
                        supabase.table("limitations").update({ "lessons": limit[0].get("lessons") + 1 }).eq("extra_id", extra[0].get("id")).execute()
                    except Exception as e:
                        print(f"Error during Supabase query (during updating user limitations): {e}")
                        return jsonify({
                            "status": False,
                            "msg": 'There has been a problem creating your lesson - contact support'
                        })
                else:
                    return jsonify({
                        "status": False,
                        "msg": 'You have reached the maximum of lessons that you can create'
                    })
            else:
                return jsonify({
                        "status": False,
                        "msg": 'The lesson you are trying to create ends before today'
                    })
        else:
            return jsonify({
                    "status": False,
                    "msg": 'A lesson with the same name already exists'
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

# TODO unique names + delete containers
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
                return jsonify({
                    "status": False,
                    "msg": 'There has been a problem canceling lesson: "' + json["lesson_name"] + '" - contact support'
                })
            
            try:
                containers = docker.containers.list(all=True)

                for container in containers:
                    if container.name.startswith(json["lesson_name"] + "-"):
                        if container.status == "running":
                            container.stop()
                        container.remove()
            except Exception as e:
                print(f"Error during deleting containers - lesson cancel: {e}")
                return jsonify({
                    "status": False,
                    "msg": 'There has been a problem canceling lesson: "' + json["lesson_name"] + '" - contact support'
                })
            
            try:
                supabase.table("limitations").update({ "lessons": limit[0].get("lessons") - 1 }).eq("extra_id", extra[0].get("id")).execute()
            except Exception as e:
                print(f"Error during Supabase query (during creation of a lesson): {e}")
                return jsonify({
                    "status": False,
                    "msg": 'There has been a problem canceling lesson: "' + json["lesson_name"] + '" - contact support'
                })
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

@bp.route('/start-container', methods=['POST'])
def start_container():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    extra = getUserExtra(user_id=json["user_id"])
    limit = getUserLimitations(user_id=json["user_id"])
    container = getContainer(id=json["container_id"])
    script = getScript(container_id=json["container_id"])

    if (extra):
        if (container and script):
            if (not limit[0].get("running_container_id") and not limit[0].get("checking_container_id")):
                c = docker.containers.get(container[0].get("name"))
                if (c):
                    args = [str(script[0].get("settings").get("cpu_load")), str(script[0].get("settings").get("network_load")), str(container[0].get("name"))]
                    command = ["python3", "container_script.py", *args] + args
                    target_cwd = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", "..", "..", "..", "Learner_scripts"))
                    process = False

                    try:
                        process = subprocess.Popen(command, cwd=target_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        print(process.pid)
                    except Exception as e:
                        return jsonify({
                                    "status": False,
                                    "msg": 'There has been a problem starting your container - contact support'
                                })

                    if (process):
                        try:
                            c.start()
                        except Exception as e:
                            process.kill()
                            return jsonify({
                                "status": False,
                                "msg": 'There has been a problem starting your container - contact support'
                            })

                        data = {
                            "pid": process.pid,
                            "running": "true",
                        }

                        try:
                            supabase.table("container_script").update(data).eq("container_id", container[0].get("id")).execute()
                        except Exception as e:
                            print(e)
                            process.kill()
                            c.stop()
                            return jsonify({
                                        "status": False,
                                        "msg": 'There has been a problem starting your container - contact support'
                                    })

                        try:
                            supabase.table("container").update({"running": "true"}).eq("id", container[0].get("id")).execute()
                        except Exception as e:
                            process.kill()
                            c.stop()
                            return jsonify({
                                        "status": False,
                                        "msg": 'There has been a problem starting your container - contact support'
                                    })

                        try:
                            supabase.table("limitations").update({"checking_container_id": container[0].get("id")}).eq("extra_id", extra[0].get("id")).execute()
                        except Exception as e:
                            process.kill()
                            c.stop()
                            return jsonify({
                                        "status": False,
                                        "msg": 'There has been a problem starting your container - contact support'
                                    })
                    else:
                        return jsonify({
                            "status": False,
                            "msg": 'There has been a problem starting your container - contact support'
                        })
                else:
                    return jsonify({
                        "status": False,
                        "msg": 'Container not found - contact support'
                    })
            else:
                return jsonify({
                    "status": False,
                    "msg": 'You can only run one container at a time stop the other container you are running - contact support'
                })
        else:
            return jsonify({
                "status": False,
                "msg": 'Container not found - contact support'
            })
    else:
        return jsonify({
            "status": False,
            "msg": 'Your user profile is incomplete - contact support'
        })
    
    return jsonify({
        "status": True,
        "msg": 'On skibidi'
        })