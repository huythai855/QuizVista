import os
import requests

from serpapi import GoogleSearch
from dotenv import load_dotenv


def download_image(image_url, save_path):
    response = requests.get(image_url)

    # Kiểm tra nếu yêu cầu thành công
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Ảnh đã được tải về và lưu tại {save_path}")
    else:
        print("Tải ảnh thất bại, mã lỗi:", response.status_code)

def get_first_image(keyword):
    params = {
        "engine": "google",  # Dùng Google search engine
        "q": keyword,  # Từ khóa tìm kiếm
        "tbm": "isch",  # Chế độ image search
        "api_key": os.getenv("SERP_API")  # Thay thế bằng API key của bạn
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    if "images_results" in results:
        return results["images_results"][0]["original"]

    return None

load_dotenv()
keyword = "President Ho Chi Minh"
image_url = get_first_image(keyword)
save_path = f"images/{keyword}.png"
download_image(image_url, save_path)
# print(os.getenv("SERP_API"))
print(image_url)
