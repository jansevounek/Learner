from flask import Blueprint, jsonify, request
from ..services.supabase_service import supabase, getUserExtra, getContainerByIdName

bp = Blueprint('container', __name__, url_prefix='/container')


@bp.route('/stop', methods=['POST'])
def get_users():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    e = getUserExtra(user_id=json["user_id"])
    extra = e[0]
    container = getContainerByIdName(json["container_name"], extra.get("id"))

    if len(container) == 0:
        return jsonify({
            "status": False,
            "msg": 'The container "' + json["container_name"] + '" that was requested for stopage could not be found'
            })
    elif len(container) >= 2:
        return jsonify({
            "status": False,
            "msg": 'More than one container with the name "' + json["container_name"] + '" have been selected for stoping - contact support'
            })
    
    if not stopContainer(json["container_name"], json["user_id"]):
        return jsonify({
            "status": False,
            "msg": 'Failed to delete container - contact support'
            })

    
    return jsonify({ 
        "status" : True,
        "body" : json["container_name"],
        "msg" : ""
        })

def stopContainer(name, user_id):
    pass