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

# gemini_api_key = os.getenv('gemini_api_key')
gemini_api_key = ""

import google.generativeai as genai
import json
from dotenv import load_dotenv

load_dotenv()
import os
from prompts import user_id_prompt, system_instruction
from tools import *

genai.configure(api_key=gemini_api_key)


class FunctionCalling():
    def __init__(self, max_token=10000, temperature=0.2):
        self.func_tools = [get_wrong_questions, list_tests, list_classes, advice_for_learning]
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

        if not function_list:
            return self.model.generate_content(user_prompt).text
        responses = {}
        for function_name, args in function_list.items():
            # Map function names to the actual function in tools
            function = globals().get(function_name)

            if callable(function):
                # Execute the function with or without arguments based on args
                if args is True:
                    result = function()  # Call without arguments
                else:
                    result = eval(f"{function_name}({args})")
                responses[function_name] = result

        print("Responses:", responses)

        response_parts = [
            genai.protos.Part(function_response=genai.protos.FunctionResponse(name=fn, response={"result": val}))
            for fn, val in responses.items()  # Use responses here to include actual function results
        ]

        response = chat.send_message(response_parts)
        return response.text




import flask
from flask import request, jsonify
app = flask.Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    request_info = request.get_json()
    print(request_info)

    user_id = request_info['user_id']
    message = request_info['message']


    agent = FunctionCalling()
    print(message, user_id)
    agent_response = agent.generate_content(message, user_id)

    response = {
        "message": agent_response
    }

    # message.append({
    #     "role": "bot",
    #     "text": agent_response
    # })



    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, port=1513)