# FastAPI for [Indic Parser](https://github.com/document-analysis-tools/indic-parser)

1. Clone the Respository
2. ```cd indic-parser-flaskapi```
3. Install all the packages ```pip install -r packages.txt```
4. Run app.py ```uvicorn app:app --reload```
5. Send <b>POST</b> request
```
curl -X 'POST'  'http://127.0.0.1:8000/ocr?inference=no&lang=san_iitb' -H 'accept: application/json'  -H 'Content-Type: multipart/form-data'  -F 'file=@path\to\image;type=image/jpeg'
```

Provide the Config File in the following format:

- ## For OCR
```
{'inference': 'no', 'lang': 'san_iitb'}
```

- ## For Layout Detection
```
{'inference': 'yes', 'lang': 'san_iitb', 'confidence_threshold':0.7, 'model': 'Sanskrit_PubLayNet_faster_rcnn'}
```
