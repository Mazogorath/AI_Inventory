## Update
2024.03.07 우분투 환경에서 opencv를 활용한 글자추출
2024.03.08 코드를 실행하기 위한 프로그래밍 환경 조성
2024.03.11 CVAT을 통해 문자 데이터셋 만들기
2024.03.12 PaddleOCR Model을 이용하여 이미지 파일의 텍스트 추출
2024.03.13 이미지의 text만 출력되게 코드 수정하고 출력되는 text정렬
2024.03.14 원하는 텍스트와 이미지를 매치하여 유/무 확인
2024.03.18 코드 설명 주석 추가


# 문자열 비교 함수
contains_any_text(texts, target_texts)

contains_text(texts, target_text)

# OCR 수행 및 텍스트 추출 함수
perform_ocr(image_path)

# 텍스트 검색 및 출력 함수
search_and_print_text(texts, target_texts)

# 이미지에 텍스트 그리기 함수
draw_text_on_image(image, texts)

## 흐름
    	1. object image의 text detecting
    	(1) PaddleOCR 모델을 이용하여 이미지의 텍스트 추출
    	(2) 추출한 글자가 해당 재고에 있는것과 비교
    	(3) 알맞은 재고를 확인 후 해당 재고의 유/무 표시
    	

## 문제점
1. 가장 잘 맞는 모델을 써도 글자 인식이 좋지 않음
