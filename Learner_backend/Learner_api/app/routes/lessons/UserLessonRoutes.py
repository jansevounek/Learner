import secrets
import string
import subprocess
import os
import signal
from flask import Blueprint, jsonify, request

from ...services.supabase_service import supabase, getUserExtra, getLesson, getContainer, getScript, getUserLimitations
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
            data = generateContainerInformation(extra, lesson)

            if (data):
                data.update({
                    "user_id": extra[0].get("id"), 
                    "lesson_id": json["lesson_id"],
                })

                container = createContainer(data, lesson)
                if (container):
                    try:
                        supabase.table("container").insert(data).execute()
                    except Exception as e:
                        print(f"Error during Supabase query (during creating container): {e}")
                        container.remove()
                        return jsonify({
                            "status": False,
                            "msg": 'There has been a problem with creating the container - contact support'
                        })
                else:
                    return jsonify({
                        "status": False,
                        "msg": 'There has been a problem with creating the container - contact support'
                    })

            else:
                return jsonify({
                    "status": False,
                    "msg": 'There has been a problem with creating the container - contact support'
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

def generateContainerInformation(extra, lesson):
    c = str(uuid.uuid4()).split("-")
    login = "guest" + c[0]
    name = lesson[0].get("name") + "-" + c[1]
    # taken from https://stackoverflow.com/questions/3854692/generate-password-in-python
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))
    p = str(8 + extra[0].get("id")) + str(lesson[0].get("id"))
    if int(p) < 8000:
        p += "1"
    data = {
        "running": "false",
        "name": name,
        "login": login,
        "password": password,
        "port": int(p)
    }

    return data

def createContainer(data, lesson):
    env_var = {
        "SIAB_PASSWORD" : data["password"],
        "SIAB_USER" : data["login"],
        "SIAB_SUDO" : "false",
        "SIAB_SSL" : "false", #TODO change this
        "SIAB_PORT" : data["port"],
        "SIAB_MESSAGES_ORIGIN" : "127.0.0.1:5173",
        "SIAB_PKGS" : "nano"
    }

    packages = ""
    for pckg in lesson[0].get("packages"):
        packages += pckg + " "

    if packages:
        env_var.update({"SIAB_PKGS" : packages[:-1]})

    ports = {
        str(data["port"]) + '/tcp': data["port"],
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
    limit = getUserLimitations(extra_id=extra[0].get("id"))
    lesson = getLesson(id=json["lesson_id"])
    container = getContainer(id=json["container_id"])

    #TODO check if process exists and start only then

    if (extra and lesson and limit):
        
        if (container):
            if (not limit[0].get("running_container_id")):
                script = getScript(container_id=json["container_id"])
                if (len(script) == 0):
                    args = [str(lesson[0].get("settings").get("cpu_load")), str(lesson[0].get("settings").get("network_load")), str(container[0].get("name"))]
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
                        c = ""
                        try:
                            c = docker.containers.get(container[0].get("name"))
                            c.start()
                        except Exception as e:
                            print(e)
                            process.kill()
                            return jsonify({
                                        "status": False,
                                        "msg": 'There has been a problem starting your container - contact support'
                                    })
                        
                        data = {
                            "container_id": container[0].get("id"),
                            "container_name": container[0].get("name"),
                            "pid": process.pid,
                            "running": "true",
                            "settings": {
                                "cpu_load": lesson[0].get("settings").get("cpu_load"),
                                "network_load": lesson[0].get("settings").get("network_load")
                            }
                        }
                        try:
                            supabase.table("container_script").insert(data).execute()
                        except Exception as e:
                            process.kill()
                            c.stop()
                            print(e)
                            return jsonify({
                                        "status": False,
                                        "msg": 'There has been a problem starting your container - contact support'
                                    })

                        try:
                            supabase.table("container").update({"running": "true"}).eq("id", container[0].get("id")).execute()
                        except Exception as e:
                            print(e)
                            process.kill()
                            c.stop()
                            return jsonify({
                                        "status": False,
                                        "msg": 'There has been a problem starting your container - contact support'
                                    })
                        
                        try:
                            supabase.table("limitations").update({"running_container_id": container[0].get("id") }).eq("extra_id", extra[0].get("id")).execute()
                        except Exception as e:
                            print(e)
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
                    args = [str(script[0].get("settings").get("cpu_load")), str(lesson[0].get("settings").get("network_load")), str(container[0].get("name"))]
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
                        c = ""
                        try:
                            c = docker.containers.get(container[0].get("name"))
                            c.start()
                        except Exception as e:
                            print(e)
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
                            supabase.table("container_script").update(data).eq("id", script[0].get("id")).execute()
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
                            print(e)
                            process.kill()
                            c.stop()
                            return jsonify({
                                        "status": False,
                                        "msg": 'There has been a problem starting your container - contact support'
                                    })
                        try:
                            supabase.table("limitations").update({"running_container_id": container[0].get("id") }).eq("extra_id", extra[0].get("id")).execute()
                        except Exception as e:
                            print(e)
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
                    "msg": 'You are currently running a different container (you can only run one container at a time)'
                })
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

@bp.route('/stop-container', methods=['POST'])
def stop_container():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    script = getScript(container_name=json["name"])
    container = getContainer(id=script[0].get("container_id"))
    limit = getUserLimitations(extra_id=container[0].get("user_id"))
    c = docker.containers.get(json["name"])
    
    if (script):
        if (limit):
            if (c):
            # taken from https://stackoverflow.com/questions/17856928/how-to-terminate-process-from-python-using-pid
                try:
                    c.stop()
                except Exception as e:
                    return jsonify({
                        "status": False,
                        "msg": 'There has been a problem stoping your container - contact support'
                    })
                
                try:
                    os.kill(script[0].get("pid"), signal.SIGTERM)
                except Exception as e:
                    return jsonify({
                        "status": False,
                        "msg": 'There has been a problem stoping your container - contact support'
                    })
                
                try:
                    supabase.table("container").update({"running": "false"}).eq("id", script[0].get("container_id")).execute()
                except Exception as e:
                    return jsonify({
                                "status": False,
                                "msg": 'There has been a problem stoping your container - contact support'
                            })
                try:
                    supabase.table("container_script").update({"running": "false"}).eq("id", script[0].get("id")).execute()
                except Exception as e:
                    return jsonify({
                                "status": False,
                                "msg": 'There has been a problem stoping your container - contact support'
                            })
                
                try:
                    supabase.table("limitations").update({"running_container_id": 0, "checking_container_id": 0}).eq("id", limit[0].get("id")).execute()
                except Exception as e:
                    return jsonify({
                                "status": False,
                                "msg": 'There has been a problem stoping your container - contact support'
                            })
            else:
                return jsonify({
                    "status": False,
                    "msg": 'No container found - contact support'
                })
        else:
            return jsonify({
                "status": False,
                "msg": 'User profile incomplete - contact support'
            })
    else:
        return jsonify({
            "status": False,
            "msg": 'No script found - contact support'
        })

    return jsonify({
        "status": True,
        "msg": 'on skibidi'
        })

@bp.route('/reset-container', methods=['POST'])
def reset_container():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    c = docker.containers.get(json["name"])
    container = getContainer(name=json["name"])
    lesson = getLesson(id=json["lesson_id"])
    limit = getUserLimitations(user_id=json["user_id"])

    if (limit):
        if limit[0].get("resets") < limit[0].get("reset_limit"):
            if (lesson):
                if (c and container):
                    if not container[0].get("running") and not c.status == "running":
                        try:
                            c.remove()
                        except Exception as e:
                            return jsonify({
                                "status": False,
                                "msg": 'There has been a problem reseting your container - contact support'
                            })

                        data = {
                            "running": "false",
                            "name": container[0].get("name"),
                            "login": container[0].get("login"),
                            "password": container[0].get("password"),
                            "port": container[0].get("port")
                        }

                        try:
                            createContainer(data, lesson)
                        except Exception as e:
                            return jsonify({
                                "status": False,
                                "msg": 'There has been a problem reseting your container - contact support'
                            })

                        try:
                            i = limit[0].get("resets") + 1
                            supabase.table("limitations").update({"resets": i}).eq("id", limit[0].get("id")).execute()
                        except Exception as e:
                            return jsonify({
                                "status": False,
                                "msg": 'There has been a problem reseting your container - contact support'
                            })

                    else:
                        return jsonify({
                            "status": False,
                            "msg": 'The container is running - contact support'
                        })
                else:
                    return jsonify({
                        "status": False,
                        "msg": 'No container found - contact support'
                    })
            else:
                return jsonify({
                    "status": False,
                    "msg": 'No lesson found - contact support'
                })
        else:
            return jsonify({
                "status": False,
                "msg": 'You have reached the maximum amount of resets'
            })
    else:
        return jsonify({
            "status": False,
            "msg": 'User profile incomplete - contact support'
        })
    
    return jsonify({
        "status": True,
        "msg": 'on skibidi'
        })