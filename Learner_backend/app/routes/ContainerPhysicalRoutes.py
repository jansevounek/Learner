from flask import Blueprint, jsonify, request
from ..services.supabase_service import supabase
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
    containers = getUserContainers(extra.get("id"))

    if extra.get("containers_allowed") >= len(containers):
        data = prepareContainerData(json["container_name"], id=1)
        if(data):
            createContainer(data)
        else:
            return jsonify({
                    "status": False,
                    "msg": "Failed to create container due to matching names"
                })

    return jsonify({"status":"done"})

# creates the non sudo container
# parameter name mandatory
# parameter id or extra mandatory
def prepareContainerData(name, **kwargs):
    id = kwargs.get("id")
    extra = kwargs.get("extra")
    # https://stackoverflow.com/questions/9390126/pythonic-way-to-check-if-something-exists
    if not extra and id:
        e = getUserExtra(extra_id=id)
        extra = e[0]
    elif not id and not extra:
        # taken from https://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python
        raise ValueError('id or user extra not provided - failed to create container.')
    
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
        "sudo" : False
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
    pass
    

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
def getUserContainers(id):
    try:
        response = supabase.table("container").select("*").eq("id", id).execute()
        return response.data
    except Exception as e:
        print(f"Error during Supabase query (during getting users containers): {e}")
        return "Error occured", 500