from flask import Blueprint, jsonify, request
from app import supabase

bp = Blueprint('physical', __name__, url_prefix='/physical')

@bp.route('/create-container', methods=['POST'])
def create_container():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    user_id = json

    print(len(getUserContainers(user_id)))
    
    return jsonify({"done":"done"})

# gets users extra information
def getUserExtra(id):
    response = supabase.client.from_("user_extra").select("*").eq("user_id", id).execute()
    return response.data

# gets all of users containers
def getUserContainers(id):
    response = supabase.client.from_("user_container").select("*").eq("user_id", id).execute()
    return response.data