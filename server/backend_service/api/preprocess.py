import base64

import requests
from flask import Blueprint, request, jsonify

# from frontend.test.view_a_test import encoded_question_set
from server.backend_service.infra.database.sqlalchemy import get_sqlalchemy


sqlalchemy_config = get_sqlalchemy()

api_preprocess = Blueprint('api_preprocess', __name__)


@api_preprocess.route("/", methods=["POST"])
def preprocess():
    # tao bo cau hoi
    body = request.get_json()
    # test_name = body['test_name']
    # test_description = body['test_description']
    input_source_type = body['input_source_type']
    content = body['content']
    content_text = ""
    generated_question_set = ""

    print(input_source_type)
    print(content)

    if input_source_type == 'file':
        # File anh -> goi den cua Vinh

        pass
    else:
        # Text -> goi den cua trung
        question_set = requests.post(
            "http://localhost:1516/rag",
            json={"message": content}
        ).json()

        print(question_set)
        # [{'answer': 'Teach Yourself Calculus', 'options': ['Teach Yourself Calculus', 'Differential Equations', 'Calculus Made Easy', 'Calculus, an Easier Book'], 'question': 'What was the title of this publication?'}, {'answer': 'Abbott, P.', 'options': ['Abbott, P.', 'Ince, E.', 'Weir, Maurice', 'Boyce, W.'], 'question': 'Who authored the Teach Yourself Calculus book?'}, {'answer': 'Theory of Ordinary Differential Equations', 'options': ['Theory of Ordinary Differential Equations', 'Differential Equations', 'Calculus', 'Calculus Made Easy'], 'question': 'How did Coddington, E. A., and Levinson, N. write their book?'}]

        formatted_question_set = []
        for question in question_set:
            formatted_question = {
                "question": question['question'],
                "answer_1": "",
                "answer_2": "",
                "answer_3": "",
                "answer_4": "",
                "correct_answer": ""
            }

            for i in range(4):
                formatted_question["answer_" + str(i)] = question['options'][i]
            formatted_question["correct_answer"] = question['answer']

            formatted_question_set.append(formatted_question)

        generated_question_set = formatted_question_set


    # tao study note, mindmap
    result_generate_note = requests.post(
        "http://localhost:1512/generate_note",
        json={"content": content}
    ).json()



    generated_note = result_generate_note['generated_note']
    generated_mindmap = result_generate_note['generated_mindmap']

    print(generated_note)
    print(generated_mindmap)

    # base 64 di cu


    # tra lai cho frontend
    # response = {
    #     "generated_note": generated_note,
    #     "generated_mindmap": generated_mindmap,
    #     "generated_question_set": generated_question_set
    # }
    #
    # print(response)

    encoded_generated_note = base64.b64encode(generated_note.encode("utf-8")).decode("utf-8")
    encoded_question_set = base64.b64encode(generated_question_set.encode("utf-8")).decode("utf-8")
    encoded_generated_mindmap = base64.b64encode(generated_mindmap.encode("utf-8")).decode("utf-8")

    response = {
        "generated_note": encoded_generated_note,
        "generated_mindmap": encoded_generated_mindmap,
        "generated_question_set": encoded_question_set
    }

    print(response)

    return jsonify(response)
