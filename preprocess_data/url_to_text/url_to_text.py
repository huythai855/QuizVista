import requests
from bs4 import BeautifulSoup

# URL của trang web cần crawl
url = "https://huythai855.github.io/"

# Gửi yêu cầu HTTP GET để lấy nội dung của trang web
response = requests.get(url)

# Kiểm tra nếu yêu cầu thành công
if response.status_code == 200:
    # Phân tích cú pháp HTML của trang web
    soup = BeautifulSoup(response.content, "html.parser")

    # Lấy tất cả văn bản từ trang
    text = soup.get_text()

    # In ra văn bản
    print(text)
else:
    print(f"Không thể truy cập trang web, mã trạng thái: {response.status_code}")
