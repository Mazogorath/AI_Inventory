# speech.py
import speech_recognition as sr
from gtts import gTTS
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
            print(f"인식된 텍스트: {text}")
            return text
        except sr.UnknownValueError:
            print("다시 말씀해 주시겠습니까?.")
            return None
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

def find_product_info(recognized_text, products):
    keyword = recognized_text.split()[0].lower()
    results = [product for product in products if keyword in product["제품 이름"].lower()]
    
    if results:
        response = "\n".join(f"{idx+1}: {product['제품 이름']}" for idx, product in enumerate(results))
        print(response)
        
        selection = input("더 자세한 정보를 보려면 번호를 입력하세요: ")
        try:
            selection = int(selection) - 1
            if 0 <= selection < len(results):
                product = results[selection]
                details = f"{product['제품 이름']}, 수량: {product['수량']}, 위치: {product['위치']}, 가격: {product['가격']}, 저자: {product['저자']}, UID: {product['UID']}"
                print(details)
                speak(details)
            else:
                print("유효하지 않은 번호입니다.")
        except ValueError:
            print("숫자를 입력해야 합니다.")
        
        return True
    else:
        response = "인식된 키워드에 해당하는 제품을 찾을 수 없습니다."
        print(response)
        speak(response)
        return False
