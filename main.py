from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from routes.auth import router as auth_router
from routes.tasks import router as task_router
import json
from mangum import Mangum
import os

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])  

@app.get("/ping")
def ping():
    return {"status": "lambda is live"}


handler = Mangum(app)

SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")