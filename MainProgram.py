from faceChecking import faceCheckings
from Whisper import main, speak
import threading
import cv2
import serial
import time
from text_detect import TEXT
from obj_detect import Object_capture

# 디버그하기 편하도록 전역화, 나중에 다 지울 예정
Indoors = []
Inventory = []
Text_books = []
Whisper_books = []
carried_out = {}
serial_port = {'A': '/dev/SomwhereA',
               'B': '/dev/SomewhereB', 'C': '/dev/SomewhereC'}
camera_id = {'A': 4, 'B': 10, 'C': 16}
count = 0


def UID_check():
    delay_time = 2
    while True:
        try:
            data = ser.readline().decode('utf-8').rstrip()
            if len(data) == 8:
                print(data)
                UID = data
                if UID not in carried_out:
                    if time.time() - delay_time > 1.0:
                        carried_out[UID] = time.time()
                        speak(f"{UID}반출등록하였습니다")
                        print(f"반출 재고 : {carried_out}")
                elif UID in carried_out:
                    if time.time() - carried_out[UID] > 5:
                        del carried_out[UID]
                        speak(f"{UID}반환되었습니다")
                        print(f"현재 재고 : {carried_out}")
                        delay_time = time.time()
        except KeyboardInterrupt:
            return


def Location_check():
    start = time.time()
    Inventory.clear()
    while True:
        data = ser.readline().decode('utf-8').rstrip()
        if len(data) == 8 and data not in Inventory:
            Inventory.append(data)
            print(data)
        if time.time() - start > 5:
            break
    print(f"현재 재고 : {Inventory}")


def Bookcapture(location):
    global Text_books, camera_id
    if location in camera_id:
        Object_capture(camera_id[location])
    time.sleep(1)
    Text_books = TEXT()
    print(Text_books)


def main_program():
    global Whisper_books
    while True:
        name, _ = faceCheckings()
        if name is not None:
            if name not in Indoors:
                Indoors.append(name)
                print(Indoors)
                speak(f"{name}님 무엇을 도와드릴까요?")
                Whisper_books = main()
                print(Whisper_books)
            elif name in Indoors:
                Indoors.remove(name)
                print(Indoors)
                speak(f"{name}님 안녕히 가세요")


def Location_check(location, Whisper_books):
    if location in serial_port:
        ser = serial.Serial(serial_port[location], baudrate=9600, timeout=1)
        for i in range(0, 100):
            data = ser.readline().decode('utf-8').rstrip()
            if len(data) == 8 and data not in Inventory:
                Inventory.append(data)
        for i in range(len(Inventory)):
            if i in Whisper_books:
                for j in range(len(Whisper_books)):
                    if Inventory[i] == Whisper_books[j][2]:
                        print("Profit!")
                        return


main_program()

# thread1 = threading.Thread(target=main_program)
# thread2 = threading.Thread(target=UID_check)
# thread3 = threading.Thread(target=Bookcapture)

# thread1.start()
# thread2.Daemon = True
# thread2.start()
# thread3.start()
