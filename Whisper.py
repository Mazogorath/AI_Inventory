import pyaudio
import wave
import whisper
from gtts import gTTS
import playsound
import sqlite3

# 녹음 함수
def record(filename="file.wav", record_seconds=5):
    format = pyaudio.paInt16
    channels = 1
    rate = 44100
    chunk = 1024
    audio = pyaudio.PyAudio()
    stream = audio.open(format=format, channels=channels,
                        rate=rate, input=True,
                        frames_per_buffer=chunk)
    print("Recording...")
    frames = []
    for i in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)
    print("Recording stopped.")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    waveFile = wave.open(filename, 'wb')
    waveFile.setnchannels(channels)
    waveFile.setsampwidth(audio.get_sample_size(format))
    waveFile.setframerate(rate)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    return filename

# Whisper를 이용한 음성 인식 함수
def transcribe_audio(filename="file.wav"):
    model = whisper.load_model("small") 
    result = model.transcribe(filename, language="ko")
    return result["text"]

# 텍스트를 음성으로 변환하고 재생하는 함수
def speak(text):
    tts = gTTS(text=text, lang='ko')
    filename = 'response.mp3'
    tts.save(filename)
    playsound.playsound(filename)

# 데이터베이스에서 제품 정보 조회 함수 (개선)
def find_product_info(recognized_text):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # 사용자의 입력에서 첫 번째 단어를 키워드로 추출
    keyword = recognized_text.split()[0].lower()  # 공백을 기준으로 나누고, 첫 번째 단어를 소문자로 변환
    
    # 데이터베이스에서 키워드를 포함하는 제품 이름 찾기
    cursor.execute("SELECT product, quantity, location FROM inventory WHERE lower(product) LIKE ?", ('%' + keyword + '%',))
    results = cursor.fetchall()
    conn.close()
    
    if results:  # 결과가 있는 경우
        for product_name, quantity, location in results:
            response = f"{product_name}는 {quantity}개 있고, {location}에 있습니다."
            print(response)
            speak(response)  # 실제 구현 환경에서는 이 줄의 주석을 제거하세요.
    else:  # 결과가 없는 경우
        response = "인식된 키워드에 해당하는 제품을 찾을 수 없습니다."
        print(response)
        speak(response)  # 실제 구현 환경에서는 이 줄의 주석을 제거하세요.


# 메인 실행 함수
def main():
    filename = record()  # 녹음 실행
    recognized_text = transcribe_audio(filename)  # 음성 파일을 텍스트로 변환
    print(f"인식된 텍스트: {recognized_text}")
    find_product_info(recognized_text)  # 데이터베이스에서 제품 정보 조회 및 음성 출력

if __name__ == "__main__":
    while True:
        main()
