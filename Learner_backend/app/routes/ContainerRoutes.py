from flask import Blueprint, jsonify, request
from ..services.supabase_service import supabase

bp = Blueprint('container', __name__, url_prefix='/container')

@bp.route('/names', methods=['POST'])
def get_users():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    data = []
    
    try:
        r = supabase.table("user").select("*").eq("user_id", json["user_id"]).execute()
        i = r.data[0].get("id")
        response = supabase.table("container").select("*").eq("extra_id", i).execute()
        data = response.data
    except Exception as e:
        print(f"Error during Supabase query (during getting users containers): {e}")
        return "Error occured", 500

    
    return jsonify({ 
        "status" : True,
        "body" : data,
        "msg" : ""
        })