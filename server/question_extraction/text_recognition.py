import pytesseract
import cv2
import os

def get_text_from_image(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    try:
        result = pytesseract.image_to_string(img, lang='eng')
    except pytesseract.TesseractError as e:
        return False
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(result)
        
    return result
