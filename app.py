from flask import Flask, request, render_template, jsonify
import pytesseract
from pdf2image import convert_from_path
import os
from src.ocr.processing import string_to_df, draw_boxes_from_data
from PIL import Image
import base64
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', extracted_text=None)

@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    
    if not file.filename.endswith(('.pdf','.png','.jpg','.jpeg')):
        return jsonify({'error': 'Only PDF, png, jpg and jpeg files are allowed'}), 400
    
    os.makedirs('uploads', exist_ok=True)
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)
    
    if file.filename.endswith('.pdf'):
        images = convert_from_path(file_path)
        extracted_text = "\n".join([pytesseract.image_to_string(img) for img in images])
        image_draw_boxes = None
    else :
        images = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(images)
        extracted_data = pytesseract.image_to_data(images)
        extracted_data = string_to_df(extracted_data)
        extracted_data = extracted_data[extracted_data["conf"] != -1]
        image_draw_boxes = draw_boxes_from_data(images, extracted_data)
        
        buffered = BytesIO()
        image_draw_boxes.save(buffered, format="PNG")
        image_draw_boxes = base64.b64encode(buffered.getvalue()).decode()
    os.remove(file_path)  
    return render_template('index.html', extracted_text=extracted_text, image_draw_boxes = image_draw_boxes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)