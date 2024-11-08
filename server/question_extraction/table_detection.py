from img2table.document import Image
import cv2
import os

def process_image_and_get_table_bbox(img_path, output_folder="folder_check", output_filename="table_detect.png"):
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Load the image
    img = Image(src=img_path)
    table_img = cv2.imread(img_path)
    
    # Extract tables
    extracted_tables = img.extract_tables()
    
    # Initialize variables for overall table bounding box
    min_x1 = min_y1 = float('inf')
    max_x2 = max_y2 = float('-inf')
    
    # Draw rectangles around the cells and calculate table bounding box
    for table in extracted_tables:
        for row in table.content.values():
            for cell in row:
                # Update overall bounding box
                min_x1 = min(min_x1, cell.bbox.x1)
                min_y1 = min(min_y1, cell.bbox.y1)
                max_x2 = max(max_x2, cell.bbox.x2)
                max_y2 = max(max_y2, cell.bbox.y2)
                
                # Draw rectangle around each cell
                cv2.rectangle(table_img, (cell.bbox.x1, cell.bbox.y1), (cell.bbox.x2, cell.bbox.y2), (255, 0, 0), 2)
    
    # Draw rectangle around the entire table
    cv2.rectangle(table_img, (min_x1, min_y1), (max_x2, max_y2), (0, 255, 0), 2)
    
    # Save the image with rectangles
    output_path = os.path.join(output_folder, output_filename)
    cv2.imwrite(output_path, table_img)
    
    # Return the bounding box of the entire table
    return (min_x1, min_y1), (max_x2, max_y2)

# Example usage
img_path = "images/pdf_6.png"
bbox = process_image_and_get_table_bbox(img_path)
print(f"Table bounding box: {bbox}")
