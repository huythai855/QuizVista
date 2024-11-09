import google.generativeai as genai
from prompt import *
import json
import os

genai.configure(api_key="AIzaSyAgxFNjZ6K7CZVeShJKiWcLtYJhlNTLZus")

def return_response_alltext(content, output_path):
    model =  genai.GenerativeModel('gemini-1.5-pro-latest',
                               system_instruction=system_instruction_all_text,
                               )
    response = model.generate_content(content)
    # In ra kết quả
    json_str = (response.text).strip('```json\n').strip('```')
    # Chuyển đổi chuỗi JSON thành đối tượng Python
    response_json = json.loads(json_str)
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Lưu vào tệp JSON
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(response_json, json_file, ensure_ascii=False, indent=4)

