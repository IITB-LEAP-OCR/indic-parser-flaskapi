# Flask API for [Indic Parser](https://github.com/document-analysis-tools/indic-parser)

1. Clone the Respository
2. ```cd indic-parser-flaskapi```
3. Install all the packages ```pip install -r packages.txt```
4. Run app.py ```python app.py```
5. Send <b>POST</b> request to ngrok server with the Image and config.json file.

Provide the Config File in the following format:

- ## For OCR
```
{'inference': 'no', 'lang': 'san_iitb'}
```

- ## For Layout Detection
```
{'inference': 'yes', 'lang': 'san_iitb', 'confidence_threshold':0.7, 'model': 'Sanskrit_PubLayNet_faster_rcnn'}
```
