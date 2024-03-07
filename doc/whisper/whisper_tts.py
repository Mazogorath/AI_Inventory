import whisper
import speech_recognition as sr
from gtts import gTTS
import os
import time
import playsound

#tts
def speak(text):
     tts = gTTS(text=text, lang='ko')
     filename='voice.mp3'
     tts.save(filename)
     playsound.playsound(filename)

#재고 리스트, 출력텍스트
inventory_list = [
    {"keyword": "책", "stock": 5, "location": "A구역", "message": "도서 재고량은 5개 입니다."},
    {"keyword": "노트북", "stock": 10, "location": "B구역", "message": "노트북 재고량은 10개 입니다."},
    {"keyword": "TV", "stock": 20, "location": "B구역", "message": "TV 재고량은 20개 입니다."},
    {"keyword": "냉장고", "stock": 30, "location": "B구역", "message": "냉장고 재고량은 30개 입니다."},
    {"keyword": "위치", "stock": None, "location": "A구역", "message": "A구역에 있습니다. 안내해 드릴까요?"}
]

# 사용자 입력 시작
speak("어디 위치해 있니?")
continue_conversation = True

while continue_conversation:
    model = whisper.load_model("small")
    result = model.transcribe("voice.mp3")
    print(result["text"])
    
    # 재고 검색 및 메시지 출력
    found = False
    for item in inventory_list:
        if item["keyword"] in result["text"]:
            print(item["message"])
            speak(item["message"])
            found = True
            break
    
    # '종료' 단어 체크
    if "종료" in result["text"]:
        continue_conversation = False
        print("대화를 종료합니다.")
        speak("대화를 종료합니다.")
        break

    if not found:
        print("해당 재고는 없습니다. 다시 말씀해 주시겠습니까?")
        speak("해당 재고는 없습니다. 다시 말씀해 주시겠습니까?")


# speak("마우스는 몇개 있어?")

# model = whisper.load_model("small")
# result = model.transcribe("voice.mp3")
# print(result["text"])


# # 재고 검색 및 메시지 출력
# found = False
# for item in inventory_list:
#     if item["keyword"] in result["text"]:
#         print(item["message"])
#         speak(item["message"])
#         found = True
#         break

# if not found:
#     print("해당 재고는 없습니다. 다시 말씀해 주시겠습니까?")
#     speak("해당 재고는 없습니다. 다시 말씀해 주시겠습니까?")