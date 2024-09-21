from flask import Blueprint, jsonify, request
from ..services.supabase_service import supabase

bp = Blueprint('physical', __name__, url_prefix='/physical')

@bp.route('/create-container', methods=['POST'])
def create_container():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})

    print(getUserExtra(json["user_id"]))
    
    return jsonify({"done":"done"})

# gets users extra information
def getUserExtra(id):
    try:
        response = supabase.table("user_extra").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error during Supabase query: {e}")
        return "Error occured", 500

# gets all of users containers
def getUserContainers(id):
    #response = supabase.client.table("user_container").select("*").eq("user_id", id).execute()
    #response = supabase.table("user_extra").select("*").execute()
    return "gg"