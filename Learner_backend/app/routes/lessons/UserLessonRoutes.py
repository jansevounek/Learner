import secrets
import string
from flask import Blueprint, jsonify, request

from ...services.supabase_service import supabase, getUserExtra, getUserLimitations, getLesson
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

    if (extra and lesson):
        data = generateContainerInformation(lesson)

        if (data):
            data.update({"user_id": extra[0].get("id")})
            if createContainer(data, lesson):
                pass
                # TODO start the process that checks the load - if it is not already running + add to the database

        else:
            return jsonify({
                "status": False,
                "msg": 'There has been a problem with creating the container'
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
    p = 8000 + data["user_id"]
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
    container = docker.containers.create(
        'garo/shellinabox:latest',
        detach=True,
        environment=env_var,
        ports=ports,
        name=data["container_code"]
    )

    print(env_var)
    return True