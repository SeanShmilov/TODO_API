import uuid

tasks = [
    {"id": "1", "title": "Learn Flask", "completed": False},
    {"id": "2", "title": "Build API", "completed": False},
    {"id": "3", "title": "Test with Postman", "completed": True}
]

def get_all_tasks():
    return tasks


def get_task_by_id(id):
    for task in tasks:
        if task["id"] == id:
            return task 
        
        
def create_task(task_data):
    new_task = {
        "id": uuid.uuid4(),
        "title": task_data['title'],
        "completed": False
    }   
    tasks.append(new_task)