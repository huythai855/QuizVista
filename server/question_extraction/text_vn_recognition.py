import pytesseract
import PIL
import cv2

def get_text_from_image(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    try:
        result = pytesseract.image_to_string(img, lang='vie+equ')
    except pytesseract.TesseractError as e:
        return False
    output_path = 'folder_check/output.txt'

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(result)
        
    return result
