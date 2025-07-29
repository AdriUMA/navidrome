from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4
import subprocess
import os
from typing import Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCRIPT_PATH = "/root/downloader-service/downloader-yt.sh"
MUSIC_DIR = "/music"

# Almacenamos el estado de las tareas en memoria
download_status: Dict[str, str] = {}

class SongRequest(BaseModel):
    url: str

def run_download_task(download_id: str, url: str):
    try:
        result = subprocess.run(
            ["sh", SCRIPT_PATH, url],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            download_status[download_id] = "done"
        else:
            download_status[download_id] = f"error: {result.stderr.strip()}"
    except Exception as e:
        download_status[download_id] = f"error: {str(e)}"

@app.post("/download")
def download_song(request: SongRequest, background_tasks: BackgroundTasks):
    if not os.path.isfile(SCRIPT_PATH):
        raise HTTPException(status_code=500, detail="Script downloader_yt.sh no encontrado")

    download_id = str(uuid4())
    download_status[download_id] = "processing"

    background_tasks.add_task(run_download_task, download_id, request.url)

    return {"status": "processing", "id": download_id, "message": "Descarga en curso"}

@app.get("/status/{download_id}")
def get_status(download_id: str):
    status = download_status.get(download_id)
    if status is None:
        raise HTTPException(status_code=404, detail="ID de descarga no encontrado")
    return {"id": download_id, "status": status}
