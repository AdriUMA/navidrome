from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

SCRIPT_PATH = "/root/downloader-service/downloader-yt.sh"

class SongRequest(BaseModel):
    url: str

@app.post("/download")
def download_song(request: SongRequest):
    if not os.path.isfile(SCRIPT_PATH):
        raise HTTPException(status_code=500, detail="Script downloader-yt.sh no encontrado")

    try:
        result = subprocess.run(
            ["sh", SCRIPT_PATH, request.url],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise Exception(result.stderr)

        return {"status": "ok", "message": "Canción descargada correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al descargar: {str(e)}")
