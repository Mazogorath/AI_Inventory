import cv2
from paddleocr import PaddleOCR

def perform_ocr(image_path):
    ocr = PaddleOCR(lang="korean")
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized_image = cv2.equalizeHist(gray_image)
    result = ocr.ocr(equalized_image)
    
    texts = []
    for line in result:
        if len(line) > 0:
            text = ""
            for i in range(len(line)):
                if isinstance(line[i], list) and len(line[i]) > 0:
                    text += line[i][1][0]
            if text:
                texts.append(text)
    
    return equalized_image, texts

def draw_text_on_image(equalized_image, texts):
    for i, text in enumerate(texts):
        cv2.putText(equalized_image, text, (10, 30 + 20 * i),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
