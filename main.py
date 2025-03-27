from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from routes.auth import router as auth_router
from routes.tasks import router as task_router
import json
from mangum import Mangum

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])  

handler = Mangum(app)