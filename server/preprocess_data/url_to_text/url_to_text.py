import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL của trang web cần crawl
url = "https://huythai855.github.io/tech/how-the-economic-machine-works/"

# Gửi yêu cầu HTTP GET để lấy nội dung của trang web
response = requests.get(url)

# Kiểm tra nếu yêu cầu thành công
if response.status_code == 200:
    # Phân tích cú pháp HTML của trang web
    soup = BeautifulSoup(response.content, "html.parser")

    # Lấy tất cả văn bản từ trang
    text = soup.get_text()

    # Lấy tất cả các ảnh từ trang
    images = []
    for img in soup.find_all("img"):
        img_url = img.get("src")
        # Nếu đường dẫn ảnh là tương đối, ta chuyển nó thành tuyệt đối
        full_img_url = urljoin(url, img_url)
        images.append(full_img_url)

    # In ra danh sách các liên kết ảnh
    print("\nLiên kết ảnh trên trang web:")
    for img in images:
        print(img)

    # Tạo thư mục để lưu ảnh
    if not os.path.exists("downloaded_images"):
        os.makedirs("downloaded_images")

    # Tải và lưu các ảnh
    for idx, img_url in enumerate(images):
        try:
            img_data = requests.get(img_url).content
            # Tạo tên file
            img_name = os.path.join("downloaded_images", f"image_{idx + 1}.jpg")
            # Lưu ảnh
            with open(img_name, "wb") as img_file:
                img_file.write(img_data)
            print(f"Đã lưu ảnh: {img_name}")
        except Exception as e:
            print(f"Không thể tải ảnh từ {img_url}: {e}")

    # In ra văn bản
    print(text)
else:
    print(f"Không thể truy cập trang web, mã trạng thái: {response.status_code}")
