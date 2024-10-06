from flask import Blueprint, jsonify, request

from ...services.supabase_service import supabase, getUserExtra, getUserContainers, getContainerByIdName
from ...services.docker_service import docker

bp = Blueprint('delete', __name__, url_prefix='/delete')

@bp.route('/container', methods=['POST'])
def delete_container():
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
            "msg": 'The container "' + json["container_name"] + '" that was requested for deletion could not be found'
            })
    elif len(container) >= 2:
        return jsonify({
            "status": False,
            "msg": 'More than one container with the name "' + json["container_name"] + '" have been selected for deletion - contact support'
            })
    
    
    if not deleteContainer(json["container_name"], extra.get("id")):
        return jsonify({
            "status": False,
            "msg": 'Failed to delete container - contact support'
            })

    return jsonify({
        "status": True,
        "msg": 'Container "' + json["container_name"] + '" deleted successfully - view it using command "container ps" '
        })

# deletes the container
def deleteContainer(name, extra_id):
    container = docker.containers.get(name)
    
    if container.status == "running":
        container.stop()

    try:
        container.remove()
    except Exception as e:
        print(f"Error removal of docker container: {e}")
        return "Error occured", 500
    
    try:
        supabase.table("container").delete().eq("name", name).eq("extra_id", extra_id).execute()
    except Exception as e:
        print(f"Error removal of container table row: {e}")
        return "Error occured", 500
    
    return True