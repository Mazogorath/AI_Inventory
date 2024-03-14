from faceChecking import faceCheckings
from Whisper import main, speak
import threading
import serial
import time

Indoors = []
Inventory = []
carried_out = {}
count = 0

serial_port = '/dev/ttyACM0'
ser = serial.Serial(serial_port, baudrate=9600, timeout=1)


def main_program():
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
        except Exception as e:
            print(f"오류 발생 : {e}")


def UID_check():
    delay_time = 2
    while True:
        try:
            data = ser.readline().decode('utf-8').rstrip()
            print(data)
            if len(data) == 8:
                UID = data
                if UID not in carried_out:
                    if time.time() - delay_time > 0.5:
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
    for i in range(0, 50):
        data = ser.readline().decode('utf-8').rstrip()
        if len(data) == 8 and data not in Inventory:
            Inventory.append(data)
            print(f"현재 재고 : {Inventory}")
            print(data)


thread1 = threading.Thread(target=main_program)
thread2 = threading.Thread(target=UID_check)
thread3 = threading.Thread(target=Location_check)

thread1.start()
thread2.start()
Location_check_start = input()
if Location_check_start == 'R':
    thread3.start()

thread1.join()
thread2.join()
thread3.join()

Location_check()
