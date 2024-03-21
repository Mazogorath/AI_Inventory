import cv2

url = 'http://192.168.0.36:7000/video'

cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()

    cv2.imshow("test", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
