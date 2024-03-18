import speech_recognition as sr
from gtts import gTTS
import sqlite3
import time
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import datetime

# 음성 인식 관련 코드
def listen_to_speech(duration=3):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=duration)
        print("찾으시는 제품을 말하세요.")
        audio_data = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio_data, language='ko-KR')
            print(f"인식된 텍스트: {text}")
            return text
        except sr.UnknownValueError:
            print("다시 말씀해 주시겠습니까?.")
        except sr.RequestError as e:
            print(f"에러 {e}")
        return None

def speak(text):
    tts = gTTS(text=text, lang='ko')
    buffer = BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    audio = AudioSegment.from_file(buffer, format="mp3")
    play(audio)

def find_product_info(recognized_text):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    keyword = recognized_text.split()[0].lower()
    cursor.execute("SELECT rowid, product, quantity, location, price, author, uid FROM inventory WHERE lower(product) LIKE ?", ('%' + keyword + '%',))
    results = cursor.fetchall()
    if results:
        # 여기에서 언팩하는 필드의 수를 데이터베이스의 결과에 맞게 수정
        response = "\n".join(f"{idx+1}: {product}" for idx, (rowid, product, quantity, location, price, author, uid) in enumerate(results))
        print(response)
        
        # 사용자가 번호를 선택할 수 있도록 요청
        selection = input("더 자세한 정보를 보려면 번호를 입력하세요: ")
        try:
            selection = int(selection) - 1
            if 0 <= selection < len(results):
                _, product, quantity, location, price, author, uid = results[selection]
                print(f"선택된 제품: {product}, 수량: {quantity}, 위치: {location}, 가격: {price}, 저자: {author}, UID: {uid}")
            else:
                print("유효하지 않은 번호입니다.")
        except ValueError:
            print("숫자를 입력해야 합니다.")
        
        return True
    else:
        response = "인식된 키워드에 해당하는 제품을 찾을 수 없습니다."
        print(response)
        return False


def main():
    while True:
        recognized_text = listen_to_speech()
        if recognized_text:
            find_product_info(recognized_text)
        else:
            print("음성 인식에 실패했습니다.")

        user_input = input("계속하려면 'y'를, 종료하려면 아무 키나 누르세요: ")
        if user_input.lower() != 'y':
            break

if __name__ == "__main__":
    main()
