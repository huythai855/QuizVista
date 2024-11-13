import google.generativeai as genai
import json
from dotenv import load_dotenv
import flask
from flask import request, jsonify

# from frontend.credential.register import response

# from server.note_and_mindmap.model import gemini_api_key

load_dotenv()
import os
from prompts import user_id_prompt, system_instruction
from tools import *

gemini_api_key = os.getenv('gemini_api_key')

genai.configure(api_key=gemini_api_key)

class FunctionCalling():
    def __init__(self, max_token=10000, temperature=0.2):
        self.func_tools = [get_wrong_questions, list_tests, list_classes]
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest',
                               system_instruction=system_instruction,
                               tools=self.func_tools
                               )
        self.generation_config = genai.GenerationConfig(
                            max_output_tokens=max_token,
                            temperature=temperature,
                        )
        
    def generate_content(self, user_prompt, user_id=1):
        prompt = user_id_prompt.replace("{{$user_id}}", str(user_id))
        prompt = prompt.replace("{{$user_prompt}}", user_prompt)
        chat = self.model.start_chat()
        response = chat.send_message(prompt)

        function_list = {}
        for part in response.parts:
            if fn := part.function_call:
                args = ", ".join(f"{key}={val}" for key, val in fn.args.items())
                function_list[fn.name] = args if args else True
                
        response_parts = [
            genai.protos.Part(function_response=genai.protos.FunctionResponse(name=fn, response={"result": val}))
                for fn, val in function_list.items()
        ]

        response = chat.send_message(response_parts)
        return response.text






app = flask.Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_id = int(request.args.get('user_id'))
    request_info = request.get_json()
    print(request_info)

    message = request_info['message']
    human_message = message[-1]["text"]

    agent = FunctionCalling()
    print(human_message, user_id)
    agent_response = agent.generate_content(human_message, user_id)

    message.append({
        "role": "bot",
        "text": agent_response
    })

    return jsonify(message)


if __name__ == '__main__':
    app.run(debug=True, port=1512)