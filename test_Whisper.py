import speech_recognition as sr

products = [
    {"ID": 1, "제품 이름": "파이썬으로배우는머신러닝의교과서", "수량": 10, "위치": "A", "가격": 34000, "저자": "이토마코토", "UID": '19edde7c'},
    {"ID": 2, "제품 이름": "개발자를위한딥러닝", "수량": 5, "위치": "B", "가격": 30000, "저자": "로런스모로니", "UID": '39adde7c'},
    {"ID": 3, "제품 이름": "qt6로GUI애플리케이션만들기", "수량": 15, "위치": "C", "가격": 28000, "저자": "마틴피츠패트릭", "UID": 'e7c8b84e'},
    {"ID": 4, "제품 이름": "라즈베리파이3를활용한임베디드리눅스프로그래밍", "수량": 20, "위치": "D", "가격": 19000, "저자": "미상", "UID": 'b9e9e37c'}
]

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
                return details, response
            else:
                print("유효하지 않은 번호입니다.")
        except ValueError:
            print("숫자를 입력해야 합니다.")
        
    else:
        response = "인식된 키워드에 해당하는 제품을 찾을 수 없습니다."
        print(response)
        return None, response

def extract_location(product_info):
    location_str_start = product_info.find("위치: ") + len("위치: ")
    location_str_end = product_info.find(",", location_str_start)
    location = product_info[location_str_start:location_str_end]
    return location

def main():
    while True:
        recognized_text = listen_to_speech()
        if recognized_text:
            product_info, response = find_product_info(recognized_text, products)
            if product_info:
                location = extract_location(product_info)
                return location, product_info, response
        else:
            print("음성 인식에 실패했습니다.")

        user_input = input("계속하려면 'y'를, 종료하려면 아무 키나 누르세요: ")
        if user_input.lower() != 'y':
            break
    return None, None, None

# main 함수의 결과를 받는 코드 예시
# location, product_info, response = main()
# print(f"위치: {location}, 제품 정보: {product_info}, 응답: {response}")
if __name__ == "__main__":
    main()
    