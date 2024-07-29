from flask import Flask, request
from flask import jsonify
from flask_supabase import Supabase
from dotenv import load_dotenv, dotenv_values
from flask_cors import CORS
import uuid
import secrets
import string
import docker

import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

load_dotenv()

app.config["SUPABASE_URL"] = os.getenv("VITE_SUPABASE_URL")
app.config['SUPABASE_KEY'] = os.getenv("VITE_SUPABASE_KEY")
supabase = Supabase(app)

client = docker.from_env()

@app.route('/start-container', methods=['POST'])
def start_container():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        print(json)
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    extra = getExtra(json)
    print(extra)
    response = startContainer(extra)
    return jsonify({'status': response})

@app.route('/create-container', methods=['POST'])
def create_container():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    response = createExtra(json)

    return jsonify({'status': response})

def createExtra(json):
    container_code = str(uuid.uuid4())
    c = str(uuid.uuid4()).split("-")
    container_login = "guest" + c[0]
    # taken from https://stackoverflow.com/questions/3854692/generate-password-in-python
    alphabet = string.ascii_letters + string.digits
    container_password = ''.join(secrets.choice(alphabet) for i in range(20))
    data = {
        "user_id": json,
        "container_code": container_code,
        "container_login": container_login,
        "container_password": container_password
    }
    supabase.client.table("user_extra").insert(data).execute()
    return setupContainer(container_code, container_login, container_password, json)

def setupContainer(code, login, password, json):
    response = supabase.client.from_("user_extra").select("id").eq("user_id", json).execute()
    id = 0
    data = response.data
    if(len(data) != 1):
        return "error"
    else:
        id = data[0].get("id")
    p = 8000 + id
    env_var = {
        "SIAB_PASSWORD" : password,
        "SIAB_USER" : login,
        "SIAB_SUDO" : "false",
        "SIAB_SSL" : "false", #TODO change this
        "SIAB_PORT" : p,
        "SIAB_MESSAGES_ORIGIN" : "127.0.0.1:5173"
    }

    ports = {
        str(p) + '/tcp': p,
    }
    client.containers.create(
        'garo/shellinabox:latest',
        detach=True,
        environment=env_var,
        ports=ports,
        name=code
    )
    return "done"

def startContainer(extra):
    container = client.containers.get(extra[0].get("container_code"))
    if (container.status != "running"):
        container.start()
        supabase.client.table("user_extra").update({"container_started": "true"}).eq("user_id", extra[0].get("user_id")).execute()
        return "started"
    elif (container.status == "running"):
        return "already_started"
    else:
        supabase.client.table("user_extra").update({"container_started": "false"}).eq("user_id", extra[0].get("user_id")).execute()
        return "problem"

def getExtra(id):
    response = supabase.client.from_("user_extra").select("*").eq("user_id", id).execute()
    return response.data

if __name__ == '__main__':
    app.run(debug=True)