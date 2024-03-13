## Update
2024.03.07 우분투 환경에서 opencv를 활용한 글자추출
2024.03.08 코드를 실행하기 위한 프로그래밍 환경 조성
2024.03.11 CVAT을 통해 문자 데이터셋 만들기
2024.03.12 PaddleOCR Model을 이용하여 이미지 파일의 텍스트 추출
2024.03.13 이미지의 text만 출력되게 코드 수정하고 출력되는 text정렬

## 사물의 글자추출 프로그램


## 함수

import cv2
from paddleocr import PaddleOCR

def extract_text(ocr_result):
  """
  OCR 결과 리스트에서 문자열만 추출하는 함수

  Args:
      ocr_result: OCR 결과 리스트 (예시: [[[...], "안녕하세요"], [...]])

  Returns:
      list: 추출된 문자열들의 리스트
  """
  texts = []
  for page in ocr_result:
    if page is None:
      continue
    for line in page[:]: # 각 페이지의 라인 정보 반복
      # line[1]에는 인식된 텍스트 정보가 저장되어 있음
      text = line[1] # 라인의 텍스트 정보 추출
      texts.append(text)
  return texts # 추출된 텍스트 리스트에 추가

# 모델 초기화
ocr = PaddleOCR(lang="korean")

# 이미지 읽기
image = cv2.imread("test2.png")

# OCR 실행
result = ocr.ocr(image)

# 추출된 텍스트 리스트
extracted_texts = extract_text(result)

# 한글 문자열 변수 생성
print(extracted_texts)

# 추출된 텍스트 리스트 반복
korean_string = ""
for word, confidence in extracted_texts:
    # isalpha() 함수는 알파벳인지 확인
    for char in word:
        if char.isalpha():
            korean_string += char
print(korean_string)
# 한글 문장 출력
# print(korean_sentence)

## 흐름
    	1. object image의 text detecting
    	(1) PaddleOCR 모델을 이용하여 이미지의 텍스트 추출
    	(2) 추출한 글자가 해당 재고에 있는것과 비교
    	(3) 알맞은 재고를 확인 후 해당 재고의 유/무 표시
    	

## 문제점
1. 가장 잘 맞는 모델을 써도 글자 인식이 좋지 않음
2. 한번에 글자텍스트를 추출하여 인식률이 떨어짐
