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

