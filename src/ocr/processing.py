from PIL import ImageDraw, ImageFont
import pandas as pd
import io
def string_to_df(string_data, sep = "\s+"):
    df_data = pd.read_csv(io.StringIO(string_data), sep=sep)
    return df_data
def draw_box(image, left, top, width, height, conf, text):
    # copy of the original image to avoid overwritting
    image_with_box = image.copy()
    
    # create drawing
    draw = ImageDraw.Draw(image_with_box)
    
    # coordinates of the bounding box
    right = left + width
    bottom = top + height
    
    # draw the red rectangle
    draw.rectangle([(left, top), (right, bottom)], outline='red', width=2)
    
    # font
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    # draw text above the box
    text_to_draw = f"{text} ({conf:.2f})"
    draw.text((left, top-25), text_to_draw, fill='red', font=font)
    
    return image_with_box


def draw_boxes_from_data(image, extracted_data):
    image_draw = image.copy()
    for box in extracted_data.itertuples():
        left = box.left
        top = box.top
        width = box.width
        height = box.height
        conf = box.conf/100
        text = box.text
        image_draw = draw_box(image_draw,left,top,width,height,conf,text)
    return image_draw       