from flask import Blueprint, jsonify, request
from ..services.supabase_service import supabase
from ..services.docker_service import docker
import uuid
import string
import secrets

bp = Blueprint('physical', __name__, url_prefix='/physical')

@bp.route('/create-container', methods=['POST'])
def create_container():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    e = getUserExtra(user_id=json["user_id"])
    extra = e[0]
    containers = getUserContainers(extra_id=extra.get("id"))

    name = str(json["container_name"])
    sudo = False

    if not extra.get("premium") and name.endswith(" -s"):
        return jsonify({
                    "status": False,
                    "msg": "User has requested a new sudo container when he has not got premium"
                })
    elif extra.get("premium") and name.endswith(" -s"):
        name = name.split(" ")[0].strip()
        sudo = True

    if extra.get("containers_allowed") > len(containers):
        data = prepareContainerData(name, id=extra.get("id"), sudo=sudo)
        if(data):
            createContainer(data)
        else:
            return jsonify({
                    "status": False,
                   "msg": "Failed to create container due to matching names"
                })
    else:
        return jsonify({
                    "status": False,
                    "msg": "User has max containers"
                })

    return jsonify({"status":"done"})

# creates the non sudo container
# parameter name mandatory
# parameter id or extra mandatory
def prepareContainerData(name, **kwargs):
    # solves user extra
    id = kwargs.get("id")
    extra = kwargs.get("extra")
    # https://stackoverflow.com/questions/9390126/pythonic-way-to-check-if-something-exists
    if not extra and id:
        e = getUserExtra(extra_id=id)
        extra = e[0]
    elif not id and not extra:
        # taken from https://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python
        raise ValueError('id or user extra not provided - failed to create container.')
    
    # solves sudo
    sudo = False
    s = kwargs.get("sudo")
    if s:
        sudo = s
    
    if(nameExists(name)):
        return False

    c = str(uuid.uuid4()).split("-")
    login = "guest" + c[0]
    # taken from https://stackoverflow.com/questions/3854692/generate-password-in-python
    alphabet = string.ascii_letters + string.digits
    passw = ''.join(secrets.choice(alphabet) for i in range(20))

    data = {
        "extra_id": extra.get("id"),
        "name": name,
        "login": login,
        "pass": passw,
        "sudo" : sudo
    }

    try:
        supabase.table("container").insert(data).execute()
    except Exception as e:
        print(f"Error during Supabase insert (creating a user container): {e}")
        return "Error occured", 500
    
    return data

# checks if user is inserting a originall name not contained in the database
def nameExists(name):
    data = []
    try:
        response = supabase.table("container").select("*").eq("name", name).execute()
        data = response.data
    except Exception as e:
        print(f"Error during Supabase query (during getting user containers in veryfing name originality): {e}")
        return "Error occured", 500
    
    if len(data) > 0:
        return True
    else:
        return False

#TODO to be continued
def createContainer(data):
    # get container for id
    try:
        response = supabase.table("container").select("id").eq("name", data["name"]).execute()
        d = response.data
    except Exception as e:
        print(f"Error during Supabase query (during getting user containers in veryfing name originality): {e}")
        return "Error occured", 500
    
    p = 10000 + d[0].get("id")
    env_var = {
        "SIAB_PASSWORD" : data["pass"],
        "SIAB_USER" : data["login"],
        "SIAB_SUDO" : data["sudo"],
        "SIAB_SSL" : "false", #TODO change this
        "SIAB_PORT" : p,
        "SIAB_MESSAGES_ORIGIN" : "127.0.0.1:5173",
        "SIAB_PKGS" : "nano"
    }

    ports = {
        str(p) + '/tcp': p,
    }
    docker.containers.create(
        'garo/shellinabox:latest',
        detach=True,
        environment=env_var,
        ports=ports,
        name=data["name"]
    )

# gets users extra information
# one of extra_id or user_id is mandatory
def getUserExtra(**kwargs):
    extra_id = kwargs.get("extra_id")
    user_id = kwargs.get("user_id")
    if user_id:
        try:
            response = supabase.table("user").select("*").eq("user_id", user_id).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting user extra): {e}")
            return "Error occured", 500
    elif extra_id:
        try:
            response = supabase.table("user").select("*").eq("id", extra_id).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting user extra): {e}")
            return "Error occured", 500
    else:
        raise ValueError("user_id or extra info id not provided - failed to fetch user extra")

# gets all of users containers
def getUserContainers(**kwargs):
    extra_id = kwargs.get("extra_id")
    user_id = kwargs.get("user_id")
    id = kwargs.get("id")
    if id:
        try:
            response = supabase.table("container").select("*").eq("id", id).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting users containers): {e}")
            return "Error occured", 500
    elif user_id:
        try:
            r = supabase.table("user").select("*").eq("user_id", user_id).execute()
            i = r.data[0].get("id")
            response = supabase.table("container").select("*").eq("extra_id", i).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting users containers): {e}")
            return "Error occured", 500
    elif extra_id:
        try:
            response = supabase.table("container").select("*").eq("extra_id", extra_id).execute()
            return response.data
        except Exception as e:
            print(f"Error during Supabase query (during getting users containers): {e}")
            return "Error occured", 500
    else:
        raise ValueError("user_id, extra_id, or id not provided - failed to fetch users containers")