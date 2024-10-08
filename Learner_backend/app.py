from flask import Flask, request
from flask import jsonify
from flask_supabase import Supabase
from dotenv import load_dotenv, dotenv_values
from flask_cors import CORS
import uuid
import secrets
import string
import docker
import stripe

import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

load_dotenv()

app.config["SUPABASE_URL"] = os.getenv("VITE_SUPABASE_URL")
app.config['SUPABASE_KEY'] = os.getenv("VITE_SUPABASE_KEY")
supabase = Supabase(app)

client = docker.from_env()


#from https://docs.stripe.com/api/connected-accounts?lang=python
stripe.api_key = os.getenv("STRIPE_API_KEY")

#TODO must be changed everytime while testing
endpoint_secret= "whsec_e3d7b620f48b92afc2e8088c8104d249ed3f659475ee649ae3e07a862f1a3b51"

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

@app.route('/create-container1', methods=['POST'])
def create_container1():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    createExtra(json)

    return jsonify({'status': "done"})

@app.route('/payment-successfull', methods=['POST'])
def payment_successful():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
    )

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        user_id = session['metadata']['userId']

        supabase.client.table("user_extra").update({"premium": "true"}).eq("user_id", user_id).execute()
        
        updateToPremiumContainer(user_id)

    return jsonify({'status': 'done'})

@app.route('/create-stripe-session', methods=['POST'])
def create_session():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    id = str(json)

    session = stripe.checkout.Session.create(
        mode="payment",
        success_url="http://localhost:5173/success",
        cancel_url="http://localhost:5173/failiure",
        line_items=[{
            "price": os.getenv("STRIPE_PRICE_ID"),
            "quantity": 1
        }],
        metadata= {
            "userId": id
        }
    )

    return jsonify({'sessionId': session.id})

@app.route('/reset-container', methods=['POST'])
def reset_container():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    extra = getExtra(json)

    status = "failed"

    if extra[0].get("premium") and extra[0].get("reseted") < 5:
        resetContainer(extra)
        status = "done"
    elif extra[0].get("premium") == False and extra[0].get("reseted") < 1:
        resetContainer(extra)
        status = "done"

    return jsonify({'status': status})

def resetContainer(extra):
    container = client.containers.get(extra[0].get("container_code"))

    if container.status == "running":
        container.stop()
    
    container.remove()

    data = {
        "id": extra[0].get("id"),
        "container_code": extra[0].get("container_code"),
        "container_login": extra[0].get("container_login"),
        "container_password": extra[0].get("container_password")
    }
    createContainer(data)

    times_reseted = extra[0].get("reseted")
    times_reseted += 1
    supabase.client.table("user_extra").update({"reseted": times_reseted}).eq("user_id", extra[0].get("user_id")).execute()

    return jsonify({'status': 'done'})

def createExtra(json):
    container_code = "free-" + str(uuid.uuid4())
    c = str(uuid.uuid4()).split("-")
    container_login = "guest" + c[0]
    # taken from https://stackoverflow.com/questions/3854692/generate-password-in-python
    alphabet = string.ascii_letters + string.digits
    container_password = ''.join(secrets.choice(alphabet) for i in range(20))
    data1 = {
        "user_id": json,
        "container_code": container_code,
        "container_login": container_login,
        "container_password": container_password
    }
    supabase.client.table("user_extra").insert(data1).execute()
    extra = getExtra(json)

    data2 = {
        "id": extra[0].get("id"),
        "container_code": container_code,
        "container_login": container_login,
        "container_password": container_password
    }
    createContainer(data2)


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
    
def updateToPremiumContainer(user_id):
    extra = getExtra(user_id)

    if extra[0].get("premium"):
        container = client.containers.get(extra[0].get("container_code"))

        if container.status == "running":
            container.stop()
        
        container.remove()

        # update the supabase container data
        container_code = "premium-" + str(uuid.uuid4())
        c = str(uuid.uuid4()).split("-")
        container_login = "guest" + c[0]
        # taken from https://stackoverflow.com/questions/3854692/generate-password-in-python
        alphabet = string.ascii_letters + string.digits
        container_password = ''.join(secrets.choice(alphabet) for i in range(20))
        data1 = {
            "container_started": "false",
            "container_used": "false",
            "container_code": container_code,
            "container_login": container_login,
            "container_password": container_password
        }

        supabase.client.table("user_extra").update(data1).eq("user_id", user_id).execute()

        extra = getExtra(user_id)
        data2 = {
            "id": extra[0].get("id"),
            "container_code": container_code,
            "container_login": container_login,
            "container_password": container_password
        }
        createContainer(data2)

def createContainer(data):
    p = 8000 + data["id"]
    env_var = {
        "SIAB_PASSWORD" : data["container_password"],
        "SIAB_USER" : data["container_login"],
        "SIAB_SUDO" : "false",
        "SIAB_SSL" : "false", #TODO change this
        "SIAB_PORT" : p,
        "SIAB_MESSAGES_ORIGIN" : "127.0.0.1:5173",
        "SIAB_PKGS" : "nano"
    }

    ports = {
        str(p) + '/tcp': p,
    }
    container = client.containers.create(
        'garo/shellinabox:latest',
        detach=True,
        environment=env_var,
        ports=ports,
        name=data["container_code"]
    )

    if data["container_code"].startswith("premium-"):
        container.start()

def getExtra(id):
    response = supabase.client.from_("user_extra").select("*").eq("user_id", id).execute()
    return response.data

if __name__ == '__main__':
    app.run(debug=True)