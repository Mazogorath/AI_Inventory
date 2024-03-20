import faceChecking as face
from Whisper import main
import cv2
import serial
import time
from text_detect import text_detect
import obj_detect as obj
import person_detection as person

Indoors = []
Whisper_books = []
carried_out = {}
serial_port = {'A': '/dev/ttyACM0',
               'B': '/dev/SomewhereB', 'C': '/dev/SomewhereC'}
camera_id = {'A': 4, 'B': 10, 'C': 16}


# def Bookcapture():
#     global Text_books, camera_id
#     obj.Object_capture()


# def Location_check(location):
#     # RFID check
#     if location in serial_port:
#         ser = serial.Serial(serial_port[location], baudrate=9600, timeout=1)
#         for i in range(0, 10):
#             data = ser.readline().decode('utf-8').rstrip()
#             if len(data) == 8 and data not in Inventory:
#                 Inventory.append(data)
#                 print(data)


def UID_check(location):
    if location not in serial_port:
        print("Location error")
    delay_time = 0
    ser = serial.Serial(serial_port[location], baudrate=9600, timeout=1)
    while True:
        try:
            data = ser.readline().decode('utf-8').rstrip()
            if len(data) == 8:
                UID = data
                if UID not in carried_out:
                    if delay_time == 0 or time.time() - delay_time > 1.0:
                        carried_out[UID] = time.time()
                        print(f"반출 재고 : {carried_out}")
                        return
                elif UID in carried_out:
                    if time.time() - carried_out[UID] > 3:
                        del carried_out[UID]
                        print(f"현재 재고 : {carried_out}")
                        delay_time = time.time()
                        return
        except KeyboardInterrupt:
            return


def exitCam():
    global Indoors
    UID_check('A')
    person.person_detect()
    # name, _ = face.faceCheckings(mode="image", image=filename, ID=4)
    name, _ = face.faceCheckings(ID=4)
    if name in Indoors:
        Indoors.remove(name)
        (f"{name}님 안녕히 가세요")


def main_program():
    global Whisper_books, Indoors
    while True:
        name, _ = face.faceCheckings(ID=4)
        if name is not None:
            if name not in Indoors:
                Indoors.append(name)
                print(Indoors)
                BookNum = obj.Object_capture(4)
                print(f"현재 재고량은 {BookNum}입니다")
                check = cv2.imread("./check.jpg")
                cv2.imshow("Inventory", check)
                print(f"{name}님 무엇을 도와드릴까요?")
                Whisper_books = main()
                match_ratio = text_detect()
                if match_ratio > 0.7:
                    print(f"{Whisper_books[2]}에서 책을 찾았습니다")
                exitCam()
