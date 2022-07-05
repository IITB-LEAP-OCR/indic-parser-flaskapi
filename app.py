import os
import urllib.request
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
# from flask_ngrok import run_with_ngrok
import cv2
import numpy as np
import json
import ast
try:
 from PIL import Image
except ImportError:
 import Image

from indicparser import indic_parser

app = Flask(__name__)
# run_with_ngrok(app)

# app.secret_key = "secret key"
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'json'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return "<h1>Indic-Parser-API</h1>"

@app.route('/v0.1/layout', methods=['POST'])
def upload_file():

  # No file in request
  if 'file' not in request.files:
    resp = jsonify({'message' : 'No file part in the request', 'url': request.url})
    resp.status_code = 400
    return resp
  
  file = request.files.get('file', None)
  # config = request.files.get('config',None)
  config = request.form
  config = str(config)
  config = config[:-4]
  config = config.partition('"')[2]
  config = ast.literal_eval(config)

  # No file selected for uploading
  if file.filename == '':
    resp = jsonify({'message' : 'No file selected for uploading', 'url': request.url})
    resp.status_code = 400
    return resp
  
  # Config
  if config:
    inference = config['inference']
    lang = config['lang']
    if inference == 'yes':
      confidence_threshold = float(config['confidence_threshold'])
      model = config['model']
    else:
      confidence_threshold = None
      model = None

    # data = config.read()
    # data = ast.literal_eval(data.decode("utf-8"))
    # inference = data['inference']
    # lang = data['lang']
    # print(inference, data)
    # if inference == 'yes':
    #   confidence_threshold = float(data['confidence_threshold'])
    #   model = data['model']
    # else:
    #   confidence_threshold = None
    #   model = None

  # Image
  if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    # im = cv2.imread(filename)
    npimg = np.fromfile(file, np.uint8)
    file2 = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    file = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)
    # print(type(file2))
    # print(file2.shape)
    pil_file=Image.fromarray(file)
    output = indic_parser(inference, lang, pil_file, filename, model, confidence_threshold, file2)
    resp = jsonify({'output': output})
    resp.status_code = 201
    return resp
  else:
    resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, json'})
    resp.status_code = 400
    return resp

if __name__ == "__main__":
    app.run()
