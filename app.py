from flask import Flask, request, render_template, jsonify
import pytesseract
from pdf2image import convert_from_path
import os
from src.ocr.processing import draw_box, draw_boxes_from_data, string_to_df, save_file, extract_text_pytesseract, file_to_image, check_file, extract_data_pytesseract, overwrite_image_from_data
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
    
    supported, _ = check_file(file.filename)
    
    if not supported:
        return jsonify({'error': 'Only PDF, png, jpg and jpeg files are allowed'}), 400

    # if the folder uploads/ doesn't exist it creates it
    file_path = save_file(file)
    images = file_to_image(file_path)
    extracted_text = extract_text_pytesseract(images)
    
    if file.filename.endswith('.pdf'):
        image_draw_boxes = None
    else :
        extracted_data = extract_data_pytesseract(images)
        #image_draw_boxes = draw_boxes_from_data(images, extracted_data)
        image_draw_boxes = overwrite_image_from_data(images, extracted_data)
        buffered = BytesIO()
        image_draw_boxes.save(buffered, format="PNG")
        image_draw_boxes = base64.b64encode(buffered.getvalue()).decode()
    os.remove(file_path)  
    return render_template('index.html', extracted_text=extracted_text, image_draw_boxes = image_draw_boxes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)