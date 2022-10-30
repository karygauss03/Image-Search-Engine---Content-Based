from typing import Optional
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return "Hello World"

@app.post('/image_query')
def image_query(image: UploadFile = File([]), size: Optional[int] = 5, _from : Optional[int] = 0, candidates : Optional[int] = 100):
    return "Heello"
