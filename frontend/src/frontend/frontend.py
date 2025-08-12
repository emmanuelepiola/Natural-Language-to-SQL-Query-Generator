from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
import json

app = FastAPI(title="Frontend")

BACKEND_URL = "http://backend:8003"

templates = Jinja2Templates(directory="templates")

class LLMSearchRequest(BaseModel):
    question: str
    model: str

class AddMovieRequest(BaseModel):
    data_line: str

class SqlQueryRequest(BaseModel):
    sql_query: str

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/llm_search")
async def llm_search(request: LLMSearchRequest):
    try:
        response = requests.post(
            f"{BACKEND_URL}/search",
            json={"question": request.question, "model": request.model},
            headers={"Content-Type": "application/json"}
        )
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Backend request failed: {str(e)}")

@app.post("/api/add_movie")
async def add_movie(request: AddMovieRequest):
    try:
        response = requests.post(
            f"{BACKEND_URL}/add",
            json={"data_line": request.data_line},
            headers={"Content-Type": "application/json"}
        )
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Backend request failed: {str(e)}")

@app.get("/api/schema")
async def get_database_schema():
    try:
        response = requests.get(f"{BACKEND_URL}/schema_summary")
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Backend request failed: {str(e)}")

@app.post("/api/sql_search")
async def sql_search(request: SqlQueryRequest):
    try:
        response = requests.post(
            f"{BACKEND_URL}/sql_search",
            json={"sql_query": request.sql_query},
            headers={"Content-Type": "application/json"}
        )
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Backend request failed: {str(e)}")