import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

products = [
    {"ID": 1, "제품 이름": "파이썬으로배우는머신러닝의교과서", "수량": 10, "위치": "A", "가격": 34000, "저자": "이토마코토", "UID": '19edde7c'},
    {"ID": 2, "제품 이름": "개발자를위한머신러닝딥러닝", "수량": 5, "위치": "B", "가격": 30000, "저자": "34000", "UID": '39adde7c'},
    {"ID": 3, "제품 이름": "파이썬과Qt6로GUI애플리케이션만들기", "수량": 15, "위치": "A", "가격": 28000, "저자": "미상", "UID": 'e7c8b84e'},
    {"ID": 4, "제품 이름": "라즈베리파이3를활용한임베디드리눅스프로그래밍", "수량": 20, "위치": "C", "가격": 19000, "저자": "미상", "UID": 'b9e9e37c'}
]

# 음성 인식 함수
def listen_to_speech(duration=1):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=duration)
        print("찾으시는 제품을 말하세요.")
        audio_data = recognizer.listen(source)
        try:
            print("Loading")
            text = recognizer.recognize_google(audio_data, language='ko-KR')
            print(f"인식된 텍스트: {text}")
            return text
        except sr.UnknownValueError:
            print("다시 말씀해 주시겠습니까?.")
            return None
        except sr.RequestError as e:
            print(f"에러 {e}")
            return None

# 텍스트를 음성으로 변환하여 출력하는 함수
def speak(text):
    tts = gTTS(text=text, lang='ko')
    buffer = BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    audio = AudioSegment.from_file(buffer, format="mp3")
    play(audio)

# 제품 정보 검색 함수
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
                # speak(details)
            else:
                print("유효하지 않은 번호입니다.")
        except ValueError:
            print("숫자를 입력해야 합니다.")
        
        return details
    else:
        response = "인식된 키워드에 해당하는 제품을 찾을 수 없습니다."
        print(response)
        speak(response)
        return False

# 메인 함수
def main():
    while True:
        recognized_text = listen_to_speech()
        if recognized_text:
            find_product_info(recognized_text, products)
        else:
            print("음성 인식에 실패했습니다.")

        user_input = input("계속하려면 'y'를, 종료하려면 아무 키나 누르세요: ")
        if user_input.lower() != 'y':
            break

if __name__ == "__main__":
    main()