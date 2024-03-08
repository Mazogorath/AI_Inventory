from faceChecking import faceCheckings

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
                with open(textpath, "a") as file:
                    file.write(f"{name}\n")
    except Exception as e:
        print(f"오류 발생 : {e}")

