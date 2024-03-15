import speech_recognition as sr
from gtts import gTTS
import playsound
import sqlite3
import time
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

def listen_to_speech(duration=3):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=duration)
        print("찾으시는 제품을 말하세요.")
        audio_data = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio_data, language='ko-KR')
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
    
    # BytesIO 객체에서 오디오 데이터를 로드하고 재생
    audio = AudioSegment.from_file(buffer, format="mp3")
    play(audio)

def find_product_info(recognized_text):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    keyword = recognized_text.split()[0].lower()
    cursor.execute("SELECT rowid, product, quantity, location FROM inventory WHERE lower(product) LIKE ?", ('%' + keyword + '%',))
    results = cursor.fetchall()
    if results:
        response = "\n".join(f"{idx+1}: {product}, 수량: {quantity}, 위치: {location}" for idx, (rowid, product, quantity, location) in enumerate(results))
        print(response)
        speak(response)
        time.sleep(0.5)
    else:
        response = "인식된 키워드에 해당하는 제품을 찾을 수 없습니다."
        print(response)
        # speak(response)

def main():
    recognized_text = listen_to_speech()
    if recognized_text:
        print(f"인식된 텍스트: {recognized_text}")
        find_product_info(recognized_text)

    else:
        print("음성 인식에 실패했습니다.")

if __name__ == "__main__":
    main()
