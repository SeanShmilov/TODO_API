from flask import jsonify, request, Blueprint
from werkzeug.exceptions import NotFound, BadRequest, Conflict, UnprocessableEntity
from bson import ObjectId, errors as bson_errors
from db import db


tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks", methods=["GET"])
def get_all_tasks_route():
    tasks_list = list(db.todo.find({}))
    for task in tasks_list:
        task["_id"] = str(task["_id"])
    return jsonify(tasks_list)



# GET Task by ID
@tasks_bp.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    try:
        task = db.todo.find_one({"_id": ObjectId(task_id)})
    except bson_errors.InvalidId:
        raise BadRequest(f"Invalid ID format: {task_id}")
    
    if task:
        task["_id"] = str(task["_id"])
        return jsonify(task)
    
    raise NotFound(f"{task_id} not found")


# POST Create Task
@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)
    
    # Ensure body is JSON
    if data is None:
        raise BadRequest("request body must be json")
    
    # Ensure title is provided
    if "title" not in data:
        raise BadRequest("request body must be json")
        
    new_title = data["title"].strip()
    
    # Ensure title contains text
    if not new_title:
        raise UnprocessableEntity("title must contain text")
    
    # Check for duplicates in DB
    if db.todo.find_one({"title": new_title}):
        raise Conflict("Task with this title already exists")


    new_task = {
        "title": new_title,
        "completed": False
    }
    
    db.todo.insert_one(new_task)
    new_task["_id"] = str(new_task["_id"])
    
    return jsonify({
        "success": True,
        "data": new_task
    }), 201



# PUT Update Task
@tasks_bp.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    try:
        oid = ObjectId(task_id)
    except bson_errors.InvalidId:
        raise BadRequest(f"Invalid ID format: {task_id}")
    
    data = request.get_json(silent=True)
    if data is None:
        raise BadRequest("request body must be json")
        
    # reject unknown fields
    allowed_fields = {"title", "completed"}
    update_data = {}
    for field in data:
        if field not in allowed_fields:
            raise BadRequest(f"not allowed to pass {field}")
        update_data[field] = data[field]
            
    # check completed type
    if "completed" in data and not isinstance(data["completed"], bool):
        raise BadRequest("completed must be a boolean")

    # Update database
    result = db.todo.update_one({"_id": oid}, {"$set": update_data})
    
    if result.matched_count == 0:
        raise NotFound(f"{task_id} not found")
        
    # Fetch and return updated document
    updated_task = db.todo.find_one({"_id": oid})
    updated_task["_id"] = str(updated_task["_id"])
    return jsonify(updated_task)


# DELETE Task
@tasks_bp.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        oid = ObjectId(task_id)
    except bson_errors.InvalidId:
        raise BadRequest(f"Invalid ID format: {task_id}")
        
    result = db.todo.delete_one({"_id": oid})
    
    if result.deleted_count == 0:
        raise NotFound(f"{task_id} not found")
    
    return jsonify({"Message": f"removed task {task_id}"})
