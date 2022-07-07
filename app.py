from fastapi import FastAPI, Query, Path, File, UploadFile, Form, Depends
from starlette.requests import Request
from pydantic import BaseModel
from typing import Optional
import os
import cv2
import numpy as np
import json
import ast
try:
 from PIL import Image
except ImportError:
 import Image
import shutil
from indicparser import indic_parser

app = FastAPI()

class Item(BaseModel):
    inference: str
    lang: str
    confidence_threshold: Optional[float] = None
    model: Optional[str] = None


@app.post('/ocr')
def upload_file(file: UploadFile, config: Item = Depends()):
    print(file.filename)
    with open("temporary.png", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    img = cv2.imread("temporary.png", cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread("temporary.png", cv2.IMREAD_COLOR)
    pil_file=Image.fromarray(img)
    output = indic_parser(config.inference, config.lang, pil_file, file.filename, config.model, config.confidence_threshold, img2)
    return output
 
