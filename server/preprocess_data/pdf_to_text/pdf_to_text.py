import PyPDF2


def extract_text_from_pdf(pdf_path):
    # Mở file PDF
    with open(pdf_path, 'rb') as file:
        # Khởi tạo PdfReader
        reader = PyPDF2.PdfReader(file)
        text = ""
        # Duyệt qua từng trang và trích xuất văn bản
        for page in reader.pages:
            text += page.extract_text()
    return text

# Đường dẫn đến file PDF của bạn
pdf_path = 'ms.pdf'

# Gọi hàm để trích xuất văn bản từ PDF
extracted_text = extract_text_from_pdf(pdf_path)
print(extracted_text)
