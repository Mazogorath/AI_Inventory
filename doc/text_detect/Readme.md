## Update
2024.03.07 우분투 환경에서 opencv를 활용한 글자추출<br>
2024.03.08 코드를 실행하기 위한 프로그래밍 환경 조성<br>
2024.03.11 CVAT을 통해 문자 데이터셋 만들기<br>
2024.03.12 PaddleOCR model을 이용하여 이미지 파일의 텍스트 추출<br>

## 사물의 글자추출 프로그램


## 함수
ocr = PaddleOCR(lang = "korean") - 모델 초기화

image = cv2.imread("test04.jpg") - 이미지 불러오기

result = ocr.ocr(image) - OCR실행

# for line in result:
#     if len(line[1]) > 0:
#         print(1)
#         # print(f"텍스트: {line[0]}")
#         # print(f"신뢰도 점수: {line[1][0]}")
#     else:
#         print("빈 텍스트 라인") - 신뢰도 출력

#texts = [] - 텍스트 문자열 리스트 생성

for line in result:
    if len(line[1]) > 0:
        texts.append(line[0]) - 결과 리스트에서 텍스트 문자열만 추출
        
for text in texts:
    print(text) - 텍스트 문자열 출력
    
 ookName = line[0][1][0] - 이미지에서 뽑아낸 텍스트 문자열
print(BookName)  - 이미지에서 뽑아낸 텍스트 문자열 화면에 출력

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) - 이미지를 회색조로 변환

blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0) - 가우시안 블러 필터 적용

thresh_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1] - 이미지를 이진화 시킴

resized_image = cv2.resize(thresh_image, (640, 480)) - 이미지 크기 조정

## 흐름
    	1. object image의 text detecting
    	(1) PaddleOCR 모델을 이용하여 이미지의 텍스트 추출
    	(2) 추출한 글자가 해당 재고에 있는것과 비교
    	(3) 알맞은 재고를 확인 후 해당 재고의 유/무 표시
    	

## 문제점
1. 가장 잘 맞는 모델을 써도 글자 인식률이 조금 낮음

## 사용한 MODEL
https://github.com/PaddlePaddle/PaddleOCR.git
