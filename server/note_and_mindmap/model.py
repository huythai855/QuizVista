from prompt import *
import google.generativeai as genai
import json
from dotenv import load_dotenv
load_dotenv()
import os

gemini_api_key = os.getenv('gemini_api_key')
genai.configure(api_key=gemini_api_key)

class MindmapNoteGenerator:

    def __init__(self, input_path, output_note_path, output_mindmap_path):
        self.note_prompt = note_prompt
        self.mindmap_prompt = mindmap_prompt
        self.note_model = genai.GenerativeModel('gemini-1.5-pro-latest',
                               system_instruction=self.note_prompt,
                               )
        self.mindmap_model = genai.GenerativeModel('gemini-1.5-pro-latest',
                               system_instruction=self.mindmap_prompt,
                               )
        self.input_path = input_path
        self.content = None
        self.output_note_path = output_note_path
        self.output_mindmap_path = output_mindmap_path

    def generate_note(self):
        response = self.note_model.generate_content(self.content)
        json_str = (response.text).strip('```json\n').strip('```')
        response_json = json.loads(json_str)
        output_dir = os.path.dirname(self.output_note_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(self.output_note_path, 'w', encoding='utf-8') as json_file:
            json.dump(response_json, json_file, ensure_ascii=False, indent=4)

    def generate_mindmap(self):
        response = self.mindmap_model.generate_content(self.content)
        json_str = (response.text).strip('```json\n').strip('```')
        response_json = json.loads(json_str)
        output_dir = os.path.dirname(self.output_mindmap_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(self.output_mindmap_path, 'w', encoding='utf-8') as json_file:
            json.dump(response_json, json_file, ensure_ascii=False, indent=4)

    def read_file(self):
        with open(self.input_path, 'r') as file:
            content = file.read()
        self.content = content