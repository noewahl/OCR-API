from PIL import ImageDraw, ImageFont, Image
from pdf2image import convert_from_path
import pandas as pd
import io
import os
from typing import Union, List
import pytesseract

# list of all suported files
SUPPORTED_FILES = (".pdf", ".jpeg", ".png", ".jpg")
UPLOADS_PATH = "uploads"



def string_to_df(string_data: str, sep: str = "\s+") -> pd.DataFrame:
    """Transform pytesseract image_to_data output string into a pandas DataFrame.

    Args:
        string_data (str): String data extracted by pytesseract.image_to_data function
        sep (str, optional): Separator used to split the data. Defaults to "\s+"

    Returns:
        pd.DataFrame: DataFrame containing the parsed OCR data

    Example:
        >>> data = pytesseract.image_to_data(image)
        >>> df = string_to_df(data)
    """
    df_data = pd.read_csv(io.StringIO(string_data), sep=sep)
    return df_data


def draw_box(
    image: Image.Image,
    left: int,
    top: int,
    width: int,
    height: int,
    conf: float,
    text: str,
) -> Image.Image:
    """Draw a red rectangle with text on a PIL Image.

    Args:
        image (Image.Image): PIL Image object to draw on
        left (int): X coordinate for left side of box
        top (int): Y coordinate for top of box
        width (int): Width of the bounding box
        height (int): Height of the bounding box
        conf (float): Confidence score (between 0 and 1)
        text (str): Text to display above the box

    Returns:
        Image.Image: New image with drawn box and text

    Example:
        >>> img = Image.open("example.png")
        >>> result = draw_box(img, left=100, top=100, width=50, height=30, conf=0.95, text="Hello")
    """
    # copy of the original image to avoid overwritting
    image_with_box = image.copy()

    # create drawing
    draw = ImageDraw.Draw(image_with_box)

    # coordinates of the bounding box
    right = left + width
    bottom = top + height

    # draw the red rectangle
    draw.rectangle([(left, top), (right, bottom)], outline="red", width=2)

    # font
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    # draw text above the box
    text_to_draw = f"{text} ({conf:.2f})"
    draw.text((left, top - 25), text_to_draw, fill="red", font=font)

    return image_with_box


def draw_boxes_from_data(
    image: Image.Image, extracted_data: pd.DataFrame
) -> Image.Image:
    """Draw all bounding boxes extracted from the image with their associated text and confidence.

    Args:
        image (Image.Image): PIL Image object to draw on
        extracted_data (pd.DataFrame): DataFrame containing OCR data with columns:
            - left: X coordinate of box
            - top: Y coordinate of box
            - width: Width of box
            - height: Height of box
            - conf: Confidence score (0-100)
            - text: Detected text

    Returns:
        Image.Image: New image with all bounding boxes and texts drawn

    Example:
        >>> img = Image.open("example.png")
        >>> ocr_data = string_to_df(pytesseract.image_to_data(img))
        >>> result = draw_boxes_from_data(img, ocr_data)
    """
    image_draw = image.copy()
    for box in extracted_data.itertuples():
        left = box.left
        top = box.top
        width = box.width
        height = box.height
        conf = box.conf / 100  # Convert confidence to 0-1 range
        text = box.text
        image_draw = draw_box(image_draw, left, top, width, height, conf, text)
    return image_draw


def check_file(file_path: str) -> bool:
    """Check if the file has a supported extension and return the extension.

    Args:
        file_path (str): Path to the file to check

    Returns:
        bool: True if file has a supported extension (.pdf, .png, .jpg, .jpeg),
              False otherwise
        str: Extension name

    Example:
        >>> check_file("document.pdf")
        True, ".pdf"
        >>> check_file("image.txt")
        False, ".txt"
    """
    _, extension = os.path.splitext(file_path)
    return extension in SUPPORTED_FILES, extension

def save_file(file):
    os.makedirs(UPLOADS_PATH, exist_ok=True)
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)
    return file_path
    

def file_to_image(file_path:str)->Image.Image:
    supported, extension = check_file(file_path)
    if supported : 
        if extension == '.pdf':
            images = convert_from_path(file_path)
        else:
            images = Image.open(file_path)
        return images
    else:
        return None
            
def extract_text_pytesseract(images: Union[Image.Image, List[Image.Image]]) -> str:
    """Extract text from a single image or list of images using pytesseract.

    Args:
        image (Union[Image.Image, List[Image.Image]]): Single PIL Image or list of PIL Images

    Returns:
        str: Extracted text from the image(s)

    Example:
        >>> img = Image.open("example.png")
        >>> text = extract_text_pytesseract(img)
        >>> 
        >>> pdf_images = convert_from_path("document.pdf")
        >>> text = extract_text_pytesseract(pdf_images)
    """
    if isinstance(images, list):
        return "\n".join(pytesseract.image_to_string(img) for img in images)
    return pytesseract.image_to_string(images)

def extract_data_pytesseract(images:Image.Image)->pd.DataFrame:
    """Extract data from a single image.
    
    Args: 
        image (Image.Image): Single PIL Image
        
    Returns:
        str: Extracted data from the image in a DataFrame
        
    Example:
        >>> img = Image.open("example.png")
        >>> data = extracted_data_pytesseract(image)
        >>> data.head()
    """
    extracted_data = pytesseract.image_to_data(images)
    extracted_data = string_to_df(extracted_data)
    extracted_data = extracted_data[extracted_data["conf"] != -1]
    extracted_data = extracted_data[
    extracted_data["text"].notna() &  # Remove NaN values
    (extracted_data["text"] != "") &  # Remove empty strings
    (extracted_data["text"].str.strip() != "")  # Remove whitespace-only strings
]
    return extracted_data

def overwrite_image_from_data(image: Image.Image, extracted_data: pd.DataFrame)->Image.Image:
    """Overwrite all detected text in an image with white rectangles containing black centered text.

    Args:
        image (Image.Image): PIL Image object to process
        extracted_data (pd.DataFrame): DataFrame containing OCR data with columns:
            - left: X coordinate of box
            - top: Y coordinate of box
            - width: Width of box
            - height: Height of box
            - conf: Confidence score (0-100)
            - text: Detected text

    Returns:
        Image.Image: New image with all detected text overwritten in white rectangles

    Example:
        >>> img = Image.open("example.png")
        >>> ocr_data = extract_data_pytesseract(img)
        >>> result = overwrite_image_from_data(img, ocr_data)
    """
    image_overwrite = image.copy()
    for box in extracted_data.itertuples():
        left = box.left
        top = box.top
        width = box.width
        height = box.height
        #conf = box.conf / 100  # Convert confidence to 0-1 range
        text = box.text
        image_overwrite= overwrite(image_overwrite, left, top, width, height, text)
    return image_overwrite
    
def overwrite(
    image: Image.Image,
    left: int,
    top: int,
    width: int,
    height: int,
    text: str,
) -> Image.Image:
    """Draw a white rectangle with centered black text over the original text.

    Args:
        image (Image.Image): PIL Image object to draw on
        left (int): X coordinate for left side of box
        top (int): Y coordinate for top of box
        width (int): Width of the bounding box
        height (int): Height of the bounding box
        text (str): Text to display inside the box

    Returns:
        Image.Image: New image with text overwritten in white rectangle

    Example:
        >>> img = Image.open("example.png")
        >>> result = overwrite(img, left=100, top=100, width=50, height=30, text="Hello")
    """
    image_with_overwritten_text = image.copy()
    draw = ImageDraw.Draw(image_with_overwritten_text)

    # Draw the white rectangle
    right = left + width
    bottom = top + height
    draw.rectangle([(left, top), (right, bottom)], outline="black", width=2, fill='white')

    # Calculate initial font size based on box height
    font_size = min(height - 4, width // len(text))  # Start with box height minus padding
    
    # Binary search to find the best font size that fits
    min_size = 8  # Minimum readable size
    max_size = font_size
    best_size = min_size
    
    while min_size <= max_size:
        current_size = (min_size + max_size) // 2
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", current_size)
        except:
            font = ImageFont.load_default()
            break

        # Get text dimensions
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Check if text fits with some padding
        if text_width <= width - 4 and text_height <= height - 4:
            best_size = current_size
            min_size = current_size + 1
        else:
            max_size = current_size - 1

    # Use the best fitting font size
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", best_size)
    except:
        font = ImageFont.load_default()

    # Get final text dimensions
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Center the text
    x = left + (width - text_width) // 2
    y = top + (height - text_height) // 2

    # Draw the text
    draw.text((x, y), text, fill="black", font=font)

    return image_with_overwritten_text


