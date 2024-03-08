import cv2
import pytesseract

# 웹캠 객체 생성
cap = cv2.VideoCapture(4)

while True:
    # 웹캠으로부터 프레임 읽기
    ret, frame = cap.read()

    # 프레임 읽기 실패 시 루프 종료
    if not ret:
        break

    # 영상 처리를 위한 흑백 변환 및 이진화
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Tesseract를 이용하여 텍스트 추출
    text = pytesseract.image_to_string(thresh)

    # 추출된 텍스트 출력
    print(text)

    # 프레임 표시
    cv2.imshow('dd', frame)

    # 'Esc' 키 입력 시 루프 종료
    key = cv2.waitKey(1)
    if key == 27:
        break

# 종료
cap.release()
cv2.destroyAllWindows()
