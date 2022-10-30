from typing import Optional
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
from elasticsearch import Elasticsearch
from .config import settings
from .utils import FeatureExtractor
import io

es = Elasticsearch([{'host': settings.host, 'port': settings.port, 'scheme': settings.scheme}])
index = settings.index_name
fe = FeatureExtractor()

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
def image_query(image: UploadFile = File([]), size: Optional[int] = 10):
    # np_image = np.array(Image.open(image.file))
    # feature_vector = fe.extract(np_image)
    # return feature_vector
    image = Image.open(io.BytesIO(image.file.read()))
    feature_vector = fe.extract(image)
    body = {
        "query": {
            "elastiknn_nearest_neighbors": {
                "vec": feature_vector,
                "field": "feature_vector",
                "similarity": "angular",
                "model": "exact",
            }
        }
    }
    res = es.search(index=index, body=body, size = size)
    return res['hits']['hits']
