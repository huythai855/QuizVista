from text_recognition import get_text_from_image
from llm import return_response_alltext
from dla import get_image_position, merge_image_and_table_detection
from white_box import extract_bounding_boxes
from image_text_matching import image_text_matching

image_path = 'images/statistic.png'
output_path = "Output/output.txt"
text_path = 'Output/response.json'
image_folder = 'Output'

# OCR text and generate a question
text_ocr = get_text_from_image(image_path, output_path)
return_response_alltext(text_ocr, text_path)

# Identify a table and a figure in image
image_position, table_position = get_image_position(image_path)
image_and_table_position = merge_image_and_table_detection(image_position, table_position)

if (len(image_and_table_position) > 0):
    # Lưu lại các image đã được DLA detect
    extract_bounding_boxes(image_path, image_position)
    image_text_matching(text_path, image_folder)
