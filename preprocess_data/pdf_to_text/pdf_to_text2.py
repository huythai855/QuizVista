import fitz  # PyMuPDF
import io
from PIL import Image


def extract_text_and_images_from_pdf(pdf_path):
    # Mở file PDF
    document = fitz.open(pdf_path)
    text = ""
    images = []

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        # Trích xuất văn bản
        text += page.get_text()

        # Trích xuất hình ảnh
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            image_path = f"image_page{page_num + 1}_{img_index + 1}.png"
            image.save(image_path)
            images.append(image_path)

    return text, images


# Đường dẫn đến file PDF của bạn
pdf_path = 'dz.pdf'

# Gọi hàm để trích xuất văn bản và hình ảnh từ PDF
extracted_text, extracted_images = extract_text_and_images_from_pdf(pdf_path)

print("Extracted Text:")
print(extracted_text)

print("Extracted Images:")
for img_path in extracted_images:
    print(f"Image saved at: {img_path}")
