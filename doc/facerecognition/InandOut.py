from faceChecking import faceCheckings
import threading
import cv2

Indoors = []
textpath = "./Text/Indoors.txt"
lock = threading.Lock()
event = threading.Event()


def ComingIn():
    while True:
        try:
            name, _ = faceCheckings()
            if name is not None:
                with lock:  # 잠금 획득
                    if name not in Indoors:
                        Indoors.append(name)
                        print(Indoors)
                        with open(textpath, "a") as file:
                            file.write(f"{name}\n")
            if event.is_set():
                break
        except Exception as e:
            print(f"오류 발생 : {e}")
            break


def ComingOut():
    while True:
        try:
            name, _ = faceCheckings()
            with lock:
                if name in Indoors:
                    Indoors.remove(name)
                    print(Indoors)
            if event.is_set():
                break
        except Exception as e:
            print(f"오류 발생 : {e}")
            break


thread1 = threading.Thread(target=ComingIn)
thread2 = threading.Thread(target=ComingOut)

thread1.start()
thread2.start()

if cv2.waitKey(1) & 0xFF == ord('q'):
    event.set()

thread1.join()
thread2.join()
