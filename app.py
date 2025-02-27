from flask import Flask, request, render_template, jsonify
import pytesseract
from pdf2image import convert_from_path
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', extracted_text=None)

@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400

    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)
    images = convert_from_path(file_path)
    extracted_text = "\n".join([pytesseract.image_to_string(img) for img in images])

    os.remove(file_path)  # Nettoyage après extraction
    return render_template('index.html', extracted_text=extracted_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)