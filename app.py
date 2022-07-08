from fastapi import FastAPI, Query, Path, File, UploadFile, Form, Depends
from fastapi import Depends, FastAPI, File, Form
from pydantic import BaseModel, validator, BaseSettings, Json
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

@app.post('/ocr')
async def upload_file(file: UploadFile, 
                      inference: str = Form(...), 
                      lang: str = Form(...), 
                      model: Optional[str] = Form(None), 
                      confidence_threshold: Optional[float] = Form(None)):
    print(file.filename)
    with open("temporary.png", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    img = cv2.imread("temporary.png", cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread("temporary.png", cv2.IMREAD_COLOR)
    pil_file=Image.fromarray(img)
    output = indic_parser(inference, lang, pil_file, file.filename, model, confidence_threshold, img2)
    return output
 
