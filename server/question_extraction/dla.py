from ultralytics import YOLO
import cv2 
import os 
import json
from img2table.document import Image
from io import BytesIO
from PIL import Image as PILImage

# dựng tạm một class model để infer ra kết quả với input vào là ảnh 
'''
names: {0: 'Caption', 1: 'Footnote', 2: 'Formula', 3: 'List-item', 4: 'Page-footer', 5: 'Page-header', 
        6: 'Picture', 7: 'Section-header', 8: 'Table', 9: 'Text', 10: 'Title'}
'''
class FigureDetectionModel: 
    def __init__(self, path): 
        # khởi tạo model 
        self.model = YOLO(path)
        # màu của bbox 
        self.ENTITIES_COLORS = {
            "Caption": (191, 100, 21),
            "Footnote": (2, 62, 115),
            "Formula": (140, 80, 58),
            "List-item": (168, 181, 69),
            "Page-footer": (2, 69, 84),
            "Page-header": (83, 115, 106),
            "Picture": (255, 72, 88),
            "Section-header": (0, 204, 192),
            "Table": (116, 127, 127),
            "Text": (0, 153, 221),
            "Title": (196, 51, 2)
        }
        # những box nằm trong ảnh doc
        self.image_in_img = []
        # những box text nằm trong ảnh doc
        self.text_in_img = []
        # vị trí của ảnh - return (top left - bottom right)
        self.img_position = {}
        self.table_position = []
        self.BOX_PADDING = 2

    def detect(self, image_path, output_path="folder_check/dla_result.png"):
        # load ảnh 
        image = cv2.imread(image_path)

        if image is None: return image 
        # chạy model 
        result = self.model.predict(source = image, conf = 0.2, iou = 0.8)

        result[0].save(output_path)
        # duyệt qua từng box của ảnh 
        boxes = result[0].boxes

        for box in boxes: 
            detection_clf  = round(box.conf.item(), 2)
            cls = list(self.ENTITIES_COLORS)[int(box.cls)]

            # ví trí của box
            start_box = (int(box.xyxy[0][0]), int(box.xyxy[0][1]))
            end_box = (int(box.xyxy[0][2]), int(box.xyxy[0][3]))


            sub_img = image.copy()
            sub_img = sub_img[start_box[1]:end_box[1], start_box[0]:end_box[0]]

            if box.cls == 6: 
                self.image_in_img.append(sub_img)
                # lưu vị trí ảnh vào trong dictionary 
                self.img_position[len(self.image_in_img) - 1] =  {(start_box, end_box)}

                continue 
            if box.cls in [2, 3, 9]: 
                self.text_in_img.append(sub_img)
                continue 
    
    def table_detect(self, image_path, output_path="folder_check/tbl_result.png"):
        # Load the image
        img = Image(src=image_path)
        table_img = cv2.imread(image_path)

        extracted_tables = img.extract_tables()
        # Initialize variables for overall table bounding box
        min_x1 = min_y1 = float('inf')
        max_x2 = max_y2 = float('-inf')
        if(len(extracted_tables) > 0):
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

            cv2.imwrite(output_path, table_img)    
            # Return the bounding box of the entire table
            self.table_position.append(((min_x1, min_y1), (max_x2, max_y2)))
    # lưu lại ảnh vào trong folder_path 
    def save(self, folder_path): 
        cwd = os.getcwd()        
        folder_path = os.path.join(cwd, folder_path)
        if not os.path.exists(folder_path):
            print(1)
            return None 
        
        img_file_path = os.path.join(folder_path, "image_img")
        for i in range(len(self.image_in_img)): 
            cv2.imwrite(img_file_path + str(i) + '.png',   self.image_in_img[i])

        text_file_path = os.path.join(folder_path, "text_img")
        for i in range(len(self.text_in_img)): 
            cv2.imwrite(text_file_path + str(i) + '.png', self.text_in_img[i])

    

def get_image_position(path):
    model = FigureDetectionModel('dla.pt')
    model.detect(path)
    model.table_detect(path)
    img_position = model.img_position
    table_position = model.table_position
    if (len(table_position) == 0):
        return img_position, []
    return img_position, table_position

def merge_table_detection(img_position, table_detection):
    # Xác định khóa cuối cùng trong img_position
    if img_position:
        last_key = max(img_position.keys())
    else:
        # Nếu img_position rỗng, khởi tạo khóa đầu tiên là 0
        last_key = 0
    
    # Tạo từ điển với khóa là khóa cuối cùng và giá trị là tập hợp các tọa độ từ table_detection
    table_detection_dict = {last_key+1: set(table_detection)}

    # Cập nhật img_position với table_detection
    img_position.update(table_detection_dict)
    
    return img_position





