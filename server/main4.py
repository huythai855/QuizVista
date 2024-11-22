from crypt import methods

import flask
from flask import request, jsonify

app = flask.Flask(__name__)

@app.route('/')
def hello():
    return """
        <h1>Hướng dẫn fake backend</h1>
        <br>
        <p>/recent_wrong_questions?user_id=1 -> lấy nhưững câu sai của user1</p>
        <br>
        <p>/list_tests?user_id=1 -> Lấy kết quả những bai kiem tra gan day cua user1 </p>
        <br>
        <p>/list_classes?user_id=1 -> Lấy danh sách những lớp mầ user1 tham gia  </p>
        <br>
        <p>/who_are_you -> Lời chào của bot  </p>
    """



@app.route('/recent_wrong_questions', methods=['GET'])
def get_recent_wrong_question():
    user_id = flask.request.args.get('user_id')
    if user_id is None:
        return "Missing user_id", 400
    else:
        temp = {
            "wrong_questions": [
                {
                    "question_id": 1,
                    "question_content": "who is the first president of USA?",
                    "correct_answer": "George Washington",
                    "user_answer": "Donald Trump"
                },
                {
                    "question_id": 2,
                    "question_content": "1+1=",
                    "correct_answer": "2",
                    "user_answer": "3"
                }]
        }

        return temp


@app.route('/list_tests', methods=['GET'])
def get_recent_test_result():
    user_id = flask.request.args.get('user_id')
    if user_id is None:
        return "Missing user_id", 400
    else:
        temp = {
            [
                {
                    "test_name": "Bai kiem tra so 1",
                    "class": "Lop toan 1",
                    "test_result": "9/10",
                    "taken_date": "2021-09-01"
                },
                {
                    "test_name": "Bai kiem tra 15 phut",
                    "class": "Lop van",
                    "test_result": "2/10",
                    "taken_date": "2021-09-02"
                }
            ]
        }
        return temp

@app.route('/list_classes', methods=['GET'])
def get_list_classes():
    user_id = flask.request.args.get('user_id')
    if user_id is None:
        return "Missing user_id", 400
    else:
        temp = {
            "classes": [
                {
                    "class_id": 1,
                    "name": "Lop toan 1",
                    "description": "Lop hoc danh cho hoc sinh lop 1",
                    "created_at": "2021-09-01",
                    "created_by_id": 1
                },
                {
                    "class_id": 2,
                    "name": "Lop van 2",
                    "description": "Lop hoc danh cho hoc sinh lop 2",
                    "created_at": "2021-09-02",
                    "created_by_id": 2
                }
            ]
        }
        return temp


@app.route('/who_are_you', methods=['GET'])
def who_are_you():
    return {
        "message": "Hello, I'm a AI Mentor - BotVista. I'm here to help you with your learning journey."
    }




if __name__ == '__main__':
    app.run(debug=True, port=1519)
