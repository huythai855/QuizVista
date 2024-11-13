from model import *

import flask
from flask import request, jsonify
app = flask.Flask(__name__)

@app.route('/generate_note', methods=['POST'])
def generate_note():
    request_body = request.get_json()
    content = request_body['content']
    print(content)

    agent = MindmapNoteGenerator(content)
    generated_note = agent.generate_note()
    generated_mindmap = agent.generate_mindmap()

    result = {
        "generated_note": generated_note,
        "generated_mindmap": generated_mindmap
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=1512)



