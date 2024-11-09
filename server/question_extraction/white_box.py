import cv2
import os

def extract_bounding_boxes(image_path, image_position, output_dir='Output/'):
    # Tạo thư mục để lưu các phần hình ảnh cắt ra nếu chưa tồn tại
    os.makedirs(output_dir, exist_ok=True)
    
    # Đọc hình ảnh
    image = cv2.imread(image_path)

    # Duyệt qua từng bounding box trong image_position
    for key, value in image_position.items():
        for idx, box in enumerate(value):
            top_left, bottom_right = box
            x1, y1 = top_left
            x2, y2 = bottom_right
            
            # Cắt phần hình ảnh trong bounding box
            cropped_image = image[y1:y2, x1:x2]
            
            # Tạo tên file cho phần hình ảnh đã cắt
            cropped_filename = f"{key}.png"
            cropped_path = os.path.join(output_dir, cropped_filename)
            
            # Lưu phần hình ảnh đã cắt
            cv2.imwrite(cropped_path, cropped_image)
    
    print(f"Extracted images saved in: {output_dir}")