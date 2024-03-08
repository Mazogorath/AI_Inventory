from faceChecking import faceCheckings
from ComingIn import Indoors


while True:
    # filename = 날짜 + 시간 + 직원 이름
    name, frame = faceCheckings()

    # 만약 출구쪽 RFID가 물건을 찍으면
    # cv2.imwrite(name, frame)
    try:
        name, _ = faceCheckings()
        if name in Indoors:
            Indoors.remove(name)
            print(Indoors)
    except Exception as e:
        print(f"오류 발생 : {e}")

