from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False

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

@app.get("/tasks/", response_model = List[Task])
def get_tasks():
    return tasks

@app.post("/tasks/")
def create_task(task: Task):
    n = len(tasks)
    id, task_id = len(tasks)
    title = task.title
    description = task.description
    completed = task.completed
    tasks[task_id] = Task(id=id, title = title, description = description, completed = completed)
    return task



@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    complete = tasks.pop(task_id, None)
    return {"message": "Task deleted", "task": complete}
