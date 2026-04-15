from flask import jsonify, request, Blueprint
from werkzeug.exceptions import NotFound, BadRequest, Conflict, HTTPException
import uuid


tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(get_all_tasks())



@tasks_bp.route("/tasks", methods=["GET"])
def get_all_tasks():
    return jsonify(tasks)


# GET Task by ID
@tasks_bp.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    # Search for the task in the list
    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if task:
        return jsonify(task)
    
    raise NotFound("Task not found")


# POST Create Task
@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    
    # Ensure title is provided
    if not data or "title" not in data:
        raise BadRequest("Title is required")
    
    new_title = data["title"]
    
    for t in tasks:
        if t["title"] == new_title:
            raise Conflict("Task with this title already exists")

    new_task = {
        "id": str(uuid.uuid4()),
        "title": data["title"],
        "completed": False
    }
    
    tasks.append(new_task)
    
    return jsonify(new_task), 201


# PUT Update Task
@tasks_bp.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if not task:
        raise NotFound("Task not found")
    
    data = request.json
    # Update fields if they exist in the request
    if "title" in data:
        task["title"] = data["title"]
    if "completed" in data:
        task["completed"] = data["completed"]
        
    return jsonify(task)


# DELETE Task
@tasks_bp.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if not task:
        raise NotFound("Task not found")
    
    tasks = [t for t in tasks if t["id"] != task_id]
    
    return jsonify({"message": f"Task {task_id} deleted successfully"})
