import cv2
import pytesseract
from PIL import Image, ImageDraw
import json

def search_question(source_text_path):
    with open(source_text_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    words_question_img = []
    for key, value in data.items():
        question = value.get('Câu hỏi', '')
        # Tách câu hỏi dựa trên ký tự "\n"
        parts = question.split('\n')
        first_part = parts[0]  # Lấy phần đầu tiên trước "\n"

        words_question_img.append(first_part)
    return words_question_img


def search_sentence(image_path, sentence):
    # Load image using OpenCV
    image_cv = cv2.imread(image_path)
    
    # Convert image to grayscale
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    
    # Perform OCR to extract all text from the image
    detected_text = pytesseract.image_to_string(gray, lang='vie')
    
    # Search for the sentence in the extracted text
    if sentence in detected_text:
        print(f"Sentence '{sentence}' found in the image.")
        
        # Perform OCR to get bounding box information for all text
        detection_data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT, lang='vie')
        
        # Convert the OpenCV image to a Pillow image for drawing
        image_pil = Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))
        
        # Search through the OCR data to find the sentence and draw a rectangle around it
        for i in range(len(detection_data['text'])):
            if detection_data['text'][i].startswith(sentence.split()[0]):
                words_combined = ' '.join(detection_data['text'][i:i+len(sentence.split())])
                if words_combined.startswith(sentence):
                    (x, y, w, h) = (detection_data['left'][i], detection_data['top'][i], detection_data['width'][i], detection_data['height'][i])
                    draw = ImageDraw.Draw(image_pil)
                    draw.rectangle(((x, y), (x + w, y + h)), outline="red", width=2)
                    print(f"Detected '{sentence}' at coordinates: Top-Left ({x}, {y}), Bottom-Right ({x + w}, {y + h})")
                    
                    # Print or return the top position of the first word
                    first_word_top = detection_data['top'][i]
                    print(f"Top position of the first word '{sentence.split()[0]}': {first_word_top}")
                    return first_word_top  # Return the top position if needed
        
        # Save the image with the highlighted sentence
        image_pil.save("folder_check/highlighted_sentence.png")
    else:
        print(f"Sentence '{sentence}' not found in the image.")
        return None


def search_image_belong_question(sentence_position, image_positions):
    closest_image_index = None
    smallest_difference = float('inf')
    
    for index, boxes in image_positions.items():
        # There might be multiple bounding boxes, so we iterate through the set
        for (top_left, bottom_right) in boxes:
            x1, y1 = top_left
            x2, y2 = bottom_right
            top_position = y1  # y1 is the top position of the image
            difference = abs(sentence_position - top_position)  # Calculate the difference

            # Check if this is the smallest difference we've found
            if difference < smallest_difference:
                smallest_difference = difference
                closest_image_index = index
    
    return closest_image_index

def find_and_update_json(json_path, target_phrase, new_value):
    # Đọc dữ liệu từ file JSON
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Kiểm tra từng câu hỏi và cập nhật nếu tìm thấy
    for question_key, question_value in data.items():
        if 'Câu hỏi' in question_value:
            question_text = question_value['Câu hỏi']
            if target_phrase in question_text:
                print(f"Found '{target_phrase}' in question '{question_key}'")
                question_value['link_image'] = new_value  # Thêm giá trị mới
                # Ghi dữ liệu đã cập nhật vào file JSON
                with open(json_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                print(f"Added 'link_image' to question '{question_key}'")
                return question_key  # Trả về key của câu hỏi tìm thấy
    print(f"'{target_phrase}' not found in any question")
    return None
