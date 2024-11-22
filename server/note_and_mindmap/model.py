from prompt import *
import google.generativeai as genai
import json
from dotenv import load_dotenv
load_dotenv()
import os

# gemini_api_key = os.getenv('gemini_api_key')
gemini_api_key = ""
genai.configure(api_key=gemini_api_key)

class MindmapNoteGenerator:
    def __init__(self, content):
        self.note_prompt = note_prompt
        self.mindmap_prompt = mindmap_prompt
        self.note_model = genai.GenerativeModel('gemini-1.5-pro-latest',
                               system_instruction=self.note_prompt,
                               )
        self.mindmap_model = genai.GenerativeModel('gemini-1.5-pro-latest',
                               system_instruction=self.mindmap_prompt,
                               )
        self.content = content

    def generate_note(self):
        response = self.note_model.generate_content(self.content)
        json_str = (response.text).strip('```json\n').strip('```')
        response_json = json.loads(json_str)
        return str(response_json)

    def generate_mindmap(self):
        response = self.mindmap_model.generate_content(self.content)
        json_str = (response.text).strip('```json\n').strip('```')
        response_json = json.loads(json_str)
        return str(response_json)

