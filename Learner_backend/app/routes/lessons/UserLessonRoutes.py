import secrets
import string
from flask import Blueprint, jsonify, request

from ...services.supabase_service import supabase, getUserExtra, getUserLimitations, getLesson, getContainer
from ...services.docker_service import docker

import uuid

bp = Blueprint('user_lessons', __name__, url_prefix='/lessons/user')

@bp.route('/create-container', methods=['POST'])
def create_container():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})

    extra = getUserExtra(user_id=json["user_id"])
    lesson = getLesson(id=json["lesson_id"])
    container = getContainer(extra_id=extra[0].get("id"), lesson_id=json["lesson_id"])

    if (extra and lesson):
        if (not container):
            data = generateContainerInformation(lesson)

            if (data):
                data.update({"user_id": extra[0].get("id"), "lesson_id": json["lesson_id"]})

                container = createContainer(data, lesson)
                if (container):
                    try:
                        supabase.table("container").insert(data).execute()
                    except Exception as e:
                        print(f"Error during Supabase query (during creating container): {e}")
                        container.remove()
                        return jsonify({
                            "status": False,
                            "msg": 'There has been a problem with creating the container - while inserting it into database'
                        })
                else:
                    return jsonify({
                        "status": False,
                        "msg": 'There has been a problem with creating the container - while starting it'
                    })

            else:
                return jsonify({
                    "status": False,
                    "msg": 'There has been a problem with creating the container - while generating its credentials'
                })
        else:
            return jsonify({
                "status": False,
                "msg": 'The container already exists - contact support'
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

def generateContainerInformation(lesson):
    c = str(uuid.uuid4()).split("-")
    login = "guest" + c[0]
    name = lesson[0].get("name") + "-" + c[1]
    # taken from https://stackoverflow.com/questions/3854692/generate-password-in-python
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))
    data = {
        "running": "true",
        "name": name,
        "login": login,
        "password": password,
    }

    return data

def createContainer(data, lesson):
    p = 8000 + data["user_id"] + lesson[0].get("id")
    env_var = {
        "SIAB_PASSWORD" : data["password"],
        "SIAB_USER" : data["login"],
        "SIAB_SUDO" : lesson[0].get("settings").get("sudo"),
        "SIAB_SSL" : "false", #TODO change this
        "SIAB_PORT" : p,
        "SIAB_MESSAGES_ORIGIN" : "127.0.0.1:5173",
        "SIAB_PKGS" : "nano"
    }

    ports = {
        str(p) + '/tcp': p,
    }

    try:
        container = docker.containers.create(
            'garo/shellinabox:latest',
            detach=True,
            environment=env_var,
            ports=ports,
            name=data["name"]
        )
    except Exception as e:
        print(f"Error during docker create: {e}")
        return False

    return container

@bp.route('/start-container', methods=['POST'])
def start_container():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    extra = getUserExtra(user_id=json["user_id"])
    lesson = getLesson(id=json["lesson_id"])
    container = getContainer(id=json["container_id"])

    if (extra and lesson):
        if (container):
            pass
        else:
            return jsonify({
                "status": False,
                "msg": 'The container is missing - contact support'
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