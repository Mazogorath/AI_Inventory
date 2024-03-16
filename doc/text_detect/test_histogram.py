import os
import cv2
from paddleocr import PaddleOCR
import time
import numpy as np

# 문자열 비교 함수
def contains_any_text(texts, target_texts):
    for target_text in target_texts:
        if contains_text(texts, target_text):
            return True
    return False

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

    # 이미지를 흑백으로 변환
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 히스토그램 평활화 적용
    equalized_image = cv2.equalizeHist(gray_image)

    # OCR 실행
    result = ocr.ocr(equalized_image)

    # 텍스트 문자열 리스트 생성
    texts = []

    # 결과 리스트에서 텍스트 문자열만 추출
    for line in result:
        if len(line) > 0:
            text = ""
            for i in range(len(line)):
                if isinstance(line[i], list) and len(line[i]) > 0:
                    text += line[i][1][0]
            if text:
                texts.append(text)

    return equalized_image, texts

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
def draw_text_on_image(equalized_image, texts):
    for i, text in enumerate(texts):
        cv2.putText(equalized_image, text, (10, 30 + 20 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# 두 문자열의 일치율 계산 함수
def calculate_match_ratio(str1, str2):
    set1 = set(str1)
    set2 = set(str2)
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    match_ratio = len(intersection) / len(union) * 100
    return match_ratio

# 메인 함수
def main():
    image_folder = "image_path"
    target_texts = ["머신러닝", "애플리케이션"]
    processed_images = set()
    list1 = ["파이썬과Qt6로GUI애플리케이션만들기5/e"]  # list1 생성
    list2 = []  # list2 생성

    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(image_folder, filename)
            if image_path not in processed_images:
                equalized_image, texts = perform_ocr(image_path)
                search_and_print_text(texts, target_texts)
                draw_text_on_image(equalized_image, texts)
                processed_images.add(image_path)
                print(image_path)

                # 텍스트 리스트를 파일로 저장
                output_file = os.path.join(image_folder, f"{os.path.splitext(filename)[0]}_text.txt")
                with open(output_file, "w", encoding="utf-8") as file:
                    file.write("\n".join(texts))

                # 텍스트를 list2에 추가
                list2.extend(texts)

    # list1과 list2의 첫 번째 요소를 문자열로 변환
    str1 = ''.join(list1)
    str2 = ''.join(list2)

    # 일치율 계산 및 출력
    match_ratio = calculate_match_ratio(str1, str2)
    print(f"일치율: {match_ratio:.2f}%")

if __name__ == "__main__":
    main()