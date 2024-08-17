import requests
from bs4 import BeautifulSoup
import json


def crawl_quiz(url, count):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    questions_list = []

    quiz_items = soup.find_all('div', class_='quiz_article_item')

    for item in quiz_items:
        # Lấy câu hỏi từ thuộc tính mock_quiz-question
        question_text = item.get('data-question')

        # Tìm tất cả các câu trả lời cho câu hỏi này
        answers = item.find_all('li')
        ans_list = [answer.get('data-answer') for answer in answers]  # Lấy câu trả lời từ thuộc tính mock_quiz-answer

        # Thêm câu hỏi và câu trả lời vào danh sách
        questions_list.append({
            "question": question_text,
            "ans": ans_list
        })

    # Chuyển đổi danh sách thành định dạng JSON
    json_data = json.dumps(questions_list, indent=4, ensure_ascii=False)

    # Lưu dữ liệu JSON vào file
    with open('data/questions_' + str(count) + '.json', 'w') as file:
        file.write(json_data)

    print('Crawl quiz from', url, 'successfully!')


# Đọc các URL từ file quiz_link.txt
with open('quiz_link.txt', 'r') as f:
    urls = f.readlines()

urls2 = [
 "https://www.wikihow.com/Past-Life-Regression-Test",
]

count = 0
# Loại bỏ ký tự xuống dòng và gọi hàm crawl cho mỗi URL
for url in urls:
    count += 1
    url = url.strip()
    crawl_quiz(url, count)
