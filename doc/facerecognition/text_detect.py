import cv2
from paddleocr import PaddleOCR

# 모델 초기화
ocr = PaddleOCR(lang = "korean")

# 이미지 읽기
image = cv2.imread("test04.jpg")

# OCR실행
result = ocr.ocr(image)

# 신뢰도 출력
# for line in result:
#     if len(line[1]) > 0:
#         print(1)
#         # print(f"텍스트: {line[0]}")
#         # print(f"신뢰도 점수: {line[1][0]}")
#     else:
#         print("빈 텍스트 라인")

# 텍스트 문자열 리스트 생성
texts = []

# 결과 리스트에서 텍스트 문자열만 추출
for line in result:
    if len(line[1]) > 0:
        texts.append(line[0])
        print(f"line in result = {line[0]}")

# 텍스트 문자열 출력
for text in texts:
    print(text)

# 텍스트 문자열
BookName = line[0][1][0]
print(line)
print(BookName)

# # 이미지를 회색조로 변환
# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # 가우시안 블러 필터 적용
# blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

# # 이미지 이진화
# thresh_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# # 이미지 크기 조정
# resized_image = cv2.resize(thresh_image, (640, 480))

