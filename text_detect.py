import os
import cv2
from paddleocr import PaddleOCR
import time

# 문자열 비교 함수
# def contains_any_text(texts, target_texts):
#     for target_text in target_texts:
#         if contains_text(texts, target_text):
#             return True
#     return False

def contains_text(texts, target_text):
    for text in texts:
        if target_text in text:
            return True
    return False

# OCR 수행 및 텍스트 추출 함수
def perform_ocr(image_path):
    # 모델 초기화
    ocr = PaddleOCR(lang="korean")

    # 이미지 읽기
    image = cv2.imread(image_path)

    # OCR 실행
    result = ocr.ocr(image)

    # 텍스트 문자열 리스트 생성
    texts = []

    # 결과 리스트에서 텍스트 문자열만 추출
    for line in result:
        if len(line) > 0 and isinstance(line[0], list) and len(line[0]) > 0:
            texts.append(line[0][1][0]) # + line[2][1][0])

    return image, texts

# 텍스트 검색 및 출력 함수
def search_and_print_text(texts, target_texts):
    # texts 리스트 출력
    print("인식된 텍스트:")
    for text in texts:
        print(text)

    # 특정 문자열 검색
    matched_texts = []
    for target_text in target_texts:
        if contains_text(texts, target_text):
            matched_texts.append(target_text)

    if len(matched_texts) > 0:
        print(f"{', '.join(matched_texts)}가 텍스트에 포함되어 있습니다.")
    else:
        print("검색한 문자열이 텍스트에 포함되어 있지 않습니다.")

# 이미지에 텍스트 그리기 함수
def draw_text_on_image(image, texts):
    for i, text in enumerate(texts):
        cv2.putText(image, text, (10, 30 + 20 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# 메인 함수
def TEXT():
    image_folder = "./crop_images/"
    target_texts = ["애플리케이션", "파이썬", "프로그래밍", "정복", "사물인터넷", "컴퓨터", "교과서", "머신"]
    process_images = set()

    # while True:
    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(image_folder, filename)
            print(image_path)
            if image_path not in process_images:
                image, texts = perform_ocr(image_path)
                search_and_print_text(texts, target_texts)
                draw_text_on_image(image, texts)
                process_images.add(image_path)
                cv2.imshow("Image", image)

        # key = cv2.waitKey(1) & 0xFF
        # if key == 27:
        #  break
        # time.sleep(1)  # 1초마다 새로운 이미지 확인

    # 모든 창 닫기
    cv2.destroyAllWindows()
