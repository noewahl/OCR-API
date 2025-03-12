# OCR-API

A Flask web application that performs Optical Character Recognition (OCR) on uploaded images and PDFs. The application extracts text and can display it with two visualization options: bounding boxes around detected text or text overlay on the original image.

## Features

- Support for multiple file formats (PDF, PNG, JPG, JPEG)
- Text extraction using Tesseract OCR
- PDF to image conversion
- Two visualization modes:
  - Bounding boxes around detected text
  - Text overlay with adaptive font sizing
- Clean web interface using Bootstrap
- Docker support for easy deployment
- Automatic file cleanup after processing

## Installation

### Using Docker (Recommended)

```bash
# Build the Docker image
docker build -t ocr-api .

# Run the container
docker run -p 8000:8000 ocr-api
```

### Manual Installation (macOS)

```bash
# Install Tesseract and Poppler
brew install tesseract
brew install poppler

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

## Dependencies

```pip-requirements
Flask==3.1.0
numpy==2.2.3
pandas==2.2.3
pdf2image==1.17.0
pillow==11.1.0
pytesseract==0.3.13
```

## Project Structure

```
OCR-API/
├── src/
│   └── ocr/
│       ├── __init__.py
│       └── processing.py
├── templates/
│   └── index.html
├── uploads/
├── app.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## Usage

### Using Docker

```bash
# Access the application at http://localhost:8000
docker run -p 8000:8000 ocr-api
```

### Manual Run

```bash
python app.py
```

Then open your browser and navigate to `http://localhost:8000`

## API Endpoints

- `GET /`: Main page
- `POST /extract_text`: Upload and process files
  - Accepts: PDF, PNG, JPG, JPEG
  - Returns: Extracted text and visualization

