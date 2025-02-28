from PIL import ImageDraw, ImageFont, Image
import pandas as pd
import io


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


def draw_box(image: Image.Image, left: int, top: int, width: int, height: int, 
            conf: float, text: str) -> Image.Image:
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


def draw_boxes_from_data(image: Image.Image, extracted_data: pd.DataFrame) -> Image.Image:
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
