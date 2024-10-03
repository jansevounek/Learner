from flask import Blueprint, jsonify, request
from ...services.supabase_service import supabase, getUserExtra, getUserContainers, getUserLimitations
from ...services.docker_service import docker
import uuid
import string
import secrets

bp = Blueprint('create', __name__, url_prefix='/create')

@bp.route('/container', methods=['POST'])
def create_container():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    e = getUserExtra(user_id=json["user_id"])
    extra = e[0]
    containers = getUserContainers(extra_id=extra.get("id"))
    limitations = getUserLimitations(extra_id=extra.get("id"))[0]

    name = str(json["container_name"])
    sudo = False

    if not extra.get("premium") and name.endswith(" -s"):
        return jsonify({
                    "status": False,
                    "msg": "Failed to create sudo container when user has no sudo rights"
                })
    elif extra.get("premium") and name.endswith(" -s"):
        name = name.split(" ")[0].strip()
        sudo = True

    if limitations.get("creations_limit") <= limitations.get("created"):
        return jsonify({
                    "status": False,
                    "msg": "Failed to create container due to the limit to creating containers daily has been reached"
                })

    if limitations.get("container_limit") > len(containers):
        data = prepareContainerData(name, id=extra.get("id"), sudo=sudo)
        if(data):
            createContainer(data)
        else:
            return jsonify({
                    "status": False,
                   "msg": "Failed to create container due to it matching a name of a different container"
                })
    else:
        return jsonify({
                    "status": False,
                    "msg": "Failed to create container due to the maximum number of containers per user being reached"
                })
    
    increaseCreatedCount(limitations)

    return jsonify({
        "status": True,
        "msg": 'Container "' + json["container_name"] + '" created successfully - view it using command "container ps" '
        })

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

# adds one to the times user has created a container today
def increaseCreatedCount(limitations):

    i = limitations.get("created") + 1

    try:
        supabase.table("limitations").update({"created": i}).eq("id", limitations.get("id")).execute()
    except Exception as e:
        print(f"Error during Supabase update (during increasing the number of creations): {e}")
        return "Error occured", 500