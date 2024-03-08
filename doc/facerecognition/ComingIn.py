from faceChecking import faceCheckings
from Whisper import main, speak

Indoors = []
count = 0
textpath = "./Text/Indoors.txt"

while True:
    try:
        name, _ = faceCheckings()
        if name is not None:
            if name not in Indoors:
                Indoors.append(name)
                print(Indoors)
                # 창고 내에 있는 직원들의 이름이 담긴 txt 생성, 현재는 필요 없음
                # with open(textpath, "a") as file:
                #     file.write(f"{name}\n")
                speak(f"{name}님 무엇을 도와드릴까요?")
                main()
            elif name in Indoors:
                Indoors.remove(name)
                print(Indoors)
                speak(f"{name}님 안녕히 가세요")
    except Exception as e:
        print(f"오류 발생 : {e}")
        
