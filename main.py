from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from routes.auth import router as auth_router
from routes.tasks import router as task_router
import json

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])  

class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# tasks = [
#     Task(id = 0, title = "Learning", description = "Learning all libraries and APIs", completed = False),
#     Task(id = 1, title = "Understanding", description = "Understand at least the most important topics in this program", completed = "false"),
#     Task(id = 2, title = "Prototyping", description = "Start brainstorming and building the program"),
#     Task(id = 3, title = "Build", description = "")
# ]

tasks = {
    0: Task(id = 0, title = "Learning", description = "Learning all libraries and APIs", completed = False),
    1: Task(id = 1, title = "Understanding", description = "Understand at least the most important topics in this program", completed = "false"),
    2: Task(id = 2, title = "Prototyping", description = "Start brainstorming and building the program"),
    3: Task(id = 3, title = "Build", description = "")
}

# @app.get("/tasks/", response_model = List[Task])
# def get_tasks():
#     return list(tasks.values())

# @app.post("/tasks/")
# def create_task(task: Task):
#     if not task.title.strip():
#         raise HTTPException(status_code=400, detail="Title cannot be blank")
#     tasks[task.id] = task
#     return list(task.values())



# @app.delete("/tasks/{task_id}")
# def delete_task(task_id: int):
#     if task_id not in tasks:
#         raise HTTPException(status_code=404, detail="Task ID not found")
#     complete = tasks.pop(task_id, None)
#     return {"message": "Task deleted", "task": complete}

# @app.patch("/tasks/{task_id}")
# def update_task(task_id: int, new_task: TaskUpdate):
    
#     if new_task.title is not None and not new_task.title.strip():
#         raise HTTPException(status_code=400, detail="Title cannot be blank")
#     if new_task.title:
#         new_title = new_task.title
#         tasks[task_id].title = new_task.title

#     if new_task.description:
#         new_desc = new_task.description
#         tasks[task_id].description = new_task.description
#     if new_task.completed is not None:
#         new_comp = new_task.completed
#         tasks[task_id].completed = new_task.completed
    
#     return {"message": "Task updated", "task": tasks[task_id]}
