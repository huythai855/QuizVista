import docx
import os
from PIL import Image
from io import BytesIO


def extract_text_and_images_from_docx(docx_path, output_dir):
    # Mở file DOCX
    doc = docx.Document(docx_path)

    # Biến để lưu văn bản
    text = []

    # Tạo thư mục lưu hình ảnh nếu chưa có
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Biến để đánh số hình ảnh
    image_counter = 1

    # Duyệt qua từng phần tử trong tài liệu
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)

    # Duyệt qua tất cả các phần tử
    for rel in doc.part.rels:
        if "image" in doc.part.rels[rel].target_ref:
            print(Image)
            image = doc.part.rels[rel].target_part.blob
            image_stream = BytesIO(image)
            img = Image.open(image_stream)
            image_filename = f'image_{image_counter}.png'
            image_path = os.path.join(output_dir, image_filename)
            img.save(image_path)
            text.append(f"[Image: {image_filename}]")
            image_counter += 1

    # Trả về văn bản đã trích xuất
    return '\n'.join(text)


# Đường dẫn đến file DOCX của bạn
docx_path = 'dz.docx'
# Thư mục để lưu hình ảnh
output_dir = 'output_dir'

# Gọi hàm để trích xuất văn bản và hình ảnh từ DOCX
extracted_text = extract_text_and_images_from_docx(docx_path, output_dir)
# print(extracted_text)
