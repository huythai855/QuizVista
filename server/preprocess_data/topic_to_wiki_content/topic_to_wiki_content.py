import requests
from bs4 import BeautifulSoup

# Từ khóa cần tìm kiếm
keyword = "Python (programming language)"
url = f"https://en.wikipedia.org/wiki/{keyword.replace(' ', '_')}"

# Gửi yêu cầu đến Wikipedia
response = requests.get(url)

# Kiểm tra xem yêu cầu có thành công không
if response.status_code == 200:
    # Phân tích HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Tìm phần nội dung chính của bài viết (thường nằm trong thẻ <div> có id là 'bodyContent' hoặc 'mw-content-text')
    content = soup.find('div', {'id': 'bodyContent'}) or soup.find('div', {'id': 'mw-content-text'})

    # Lấy tất cả các đoạn văn (p tags)
    paragraphs = content.find_all('p')

    # In ra từng đoạn văn
    for para in paragraphs:
        print(para.text)
else:
    print("Không thể truy cập trang Wikipedia!")
