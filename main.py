from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from routes.auth import router as auth_router
from routes.tasks import router as task_router
import json
from mangum import Mangum
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(root_path="/prod") # Change to "/" after production and testing
# app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://cloud-task-manager-bucket.s3-website-us-west-1.amazonaws.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Content-Type", "Authorization"],
)

@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request):
    print("OPTIONS caught:", request.url.path)
    response = JSONResponse(status_code=200, content="OK")
    response.headers["Access-Control-Allow-Origin"] = "http://cloud-task-manager-bucket.s3-website-us-west-1.amazonaws.com"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


app.include_router(auth_router, prefix="/auth", tags=["auth"])  
app.include_router(task_router, prefix="/tasks", tags=["tasks"])  

handler = Mangum(app)

SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")