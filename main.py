from fastapi import FastAPI
from starlette.responses import FileResponse

app = FastAPI()

@app.get('/')
def home():
    return FileResponse('index.html')

