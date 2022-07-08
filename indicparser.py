import layoutparser as lp
import pandas as pd
import numpy as np
import cv2
import os
try:
 from PIL import Image
except ImportError:
 import Image
import pytesseract
from pdf2image import convert_from_path
import sys
from pdfreader import SimplePDFViewer
import subprocess
import json
from pathlib import Path
from uuid import uuid4
from math import floor

from layout_inference import infer_layout

LEVELS = {
    'page_num': 1,
    'block_num': 2,
    'par_num': 3,
    'line_num': 4,
    'word_num': 5
}

# def create_image_url(filepath):
#   """
#   Label Studio requires image URLs, so this defines the mapping from filesystem to URLs
#   if you use ./serve_local_files.sh <my-images-dir>, the image URLs are localhost:8081/filename.png
#   Otherwise you can build links like /data/upload/filename.png to refer to the files
#   """
#   filename = os.path.basename(filepath)
#   return f'http://localhost:8081/{filename}'

def convert_to_ls(image, tesseract_output, file_name, per_level='block_num'):
  """
  :param image: PIL image object
  :param tesseract_output: the output from tesseract
  :param per_level: control the granularity of bboxes from tesseract
  :return: tasks.json ready to be imported into Label Studio with "Optical Character Recognition" template
  """
  image_width, image_height = image.size
  per_level_idx = LEVELS[per_level]
  results = []
  all_scores = []
  for i, level_idx in enumerate(tesseract_output['level']):
    if level_idx == per_level_idx:
      bbox = {
        'x': 100 * tesseract_output['left'][i] / image_width,
        'y': 100 * tesseract_output['top'][i] / image_height,
        'width': 100 * tesseract_output['width'][i] / image_width,
        'height': 100 * tesseract_output['height'][i] / image_height,
        'rotation': 0
      }

      words, confidences = [], []
      for j, curr_id in enumerate(tesseract_output[per_level]):
        if curr_id != tesseract_output[per_level][i]:
          continue
        word = tesseract_output['text'][j]
        confidence = tesseract_output['conf'][j]
        words.append(word)
        if confidence != '-1':
          confidences.append(float(confidence / 100.))

      text = ' '.join((str(v) for v in words)).strip()
      if not text:
        continue
      region_id = str(uuid4())[:10]
      score = sum(confidences) / len(confidences) if confidences else 0
      bbox_result = {
        'id': region_id, 'from_name': 'bbox', 'to_name': 'image', 'type': 'rectangle',
        'value': bbox}
      transcription_result = {
        'id': region_id, 'from_name': 'transcription', 'to_name': 'image', 'type': 'textarea',
        'value': dict(text=[text], **bbox), 'score': score}
      results.extend([bbox_result, transcription_result])
      all_scores.append(score)

  return {
    'data': {
      'ocr': file_name
    },
    'predictions': [{
      'result': results,
      'score': sum(all_scores) / len(all_scores) if all_scores else 0
    }]
  }


def indic_parser(inference_flag, lang_model, image, file_name, config_name, confidence_threshold, im):
  infer_flag = inference_flag
  tessdata_dir_config = r'--tessdata-dir "configs/tessdata"'
  os.environ["TESSDATA_PREFIX"] = 'configs/tessdata'
  languages=pytesseract.get_languages(config=tessdata_dir_config)

  if lang_model in languages:
    ocr_agent = lp.TesseractAgent(languages=lang_model)

  LEVELS = {
    'page_num': 1,
    'block_num': 2,
    'par_num': 3,
    'line_num': 4,
    'word_num': 5
  }
  if infer_flag == "no":
    # create_hocr(img_path, languages, int(linput)-1, output_path)
    res = ocr_agent.detect(image, return_response = True)
    tesseract_output = res["data"].to_dict('list')
    task = convert_to_ls(image, tesseract_output, file_name, per_level='block_num')
    return task
  else:
    out = infer_layout(config_name, im, confidence_threshold)
    return out
