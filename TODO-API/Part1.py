from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Learn Flask", "completed": False},
    {"id": 2, "title": "Build API", "completed": False},
    {"id": 3, "title": "Test with Postman", "completed": True}
]

task_id_counter = 4


#GET All Tasks
@app.route("/tasks", methods=["GET"])
def get_all_tasks():
    return jsonify(tasks)


# GET Task by ID 
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    # Search for the task in the list
    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if task:
        return jsonify(task)
    
    return jsonify({"error": "Task not found"}), 404


# POST Create Task
@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id_counter
    data = request.json
    
    # Ensure title is provided
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    new_task = {
        "id": task_id_counter,
        "title": data["title"],
        "completed": False
    }
    
    tasks.append(new_task)
    task_id_counter += 1
    
    return jsonify(new_task), 201


# PUT Update Task
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if not task:
       return jsonify({"error": "Task not found"}), 404
    
    data = request.json
  
    if "title" in data:
        task["title"] = data["title"]
    if "completed" in data:
        task["completed"] = data["completed"]
        
    return jsonify(task)


# DELETE Task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    
    tasks = [t for t in tasks if t["id"] != task_id]
    
    return jsonify({"message": f"Task {task_id} deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)