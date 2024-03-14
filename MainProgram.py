from faceChecking import faceCheckings
from Whisper import main, speak
import threading
import cv2
import serial
import time
from text_detect import TEXT
from obj_detect import Object_capture

Indoors = []
Inventory = []
carried_out = {}
count = 0
Location_start_check = 'N'

serial_port = '/dev/ttyACM0'
ser = serial.Serial(serial_port, baudrate=9600, timeout=1)


def UID_check():
    delay_time = 2
    while True:
        try:
            data = ser.readline().decode('utf-8').rstrip()
            print(data)
            if len(data) == 8:
                UID = data
                if UID not in carried_out:
                    if time.time() - delay_time > 1.0:
                        carried_out[UID] = time.time()
                        print(f"{UID}반출")
                        speak(f"{UID}반출등록하였습니다")
                        print(f"현재 재고 : {carried_out}")
                elif UID in carried_out:
                    if time.time() - carried_out[UID] > 5:
                        del carried_out[UID]
                        print(f"{UID}반환")
                        speak(f"{UID}반환되었습니다")
                        print(f"현재 재고 : {carried_out}")
                        delay_time = time.time()
        except KeyboardInterrupt:
            return


def Location_check():
    global Location_start_check
    time.sleep(0.5)
    Object_capture()
    time.sleep(0.5)
    TEXT()
    time.sleep(0.5)
    for i in range(0, 5):
        data = ser.readline().decode('utf-8').rstrip()
        if len(data) == 8 and data not in Inventory:
            Inventory.append(data)
            print(f"현재 재고 : {Inventory}")
            print(data)
    Location_start_check = 'N'


def Bookcapture():
    Object_capture()
    TEXT()


def userInput():
    global Location_start_check
    while True:
        Location_start_check = input()


def main_program():
    global Location_start_check
    while True:
        try:
            name, _ = faceCheckings()
            if name is not None:
                if name not in Indoors:
                    Indoors.append(name)
                    print(Indoors)
                    speak(f"{name}님 무엇을 도와드릴까요?")
                    main()
                elif name in Indoors:
                    Indoors.remove(name)
                    print(Indoors)
                    speak(f"{name}님 안녕히 가세요")
            if Location_start_check == 'R':
                Location_check()
                time.sleep(0.5)
        except Exception as e:
            print(f"오류 발생 : {e}")


# thread1 = threading.Thread(target=main_program)
# thread2 = threading.Thread(target=UID_check)
# thread3 = threading.Thread(target=Bookcapture)

# thread1.start()
# thread2.start()
# thread3.start()

# thread1.join()
# thread2.join()
# thread3.join()
