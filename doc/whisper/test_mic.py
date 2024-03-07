import pyaudio
import wave
import whisper

def record(filename="file.wav", record_seconds=5):
    # 녹음 설정
    format = pyaudio.paInt16
    channels = 1
    rate = 44100
    chunk = 1024

    audio = pyaudio.PyAudio()

    # 마이크에서 오디오 스트림 시작
    stream = audio.open(format=format, channels=channels,
                        rate=rate, input=True,
                        frames_per_buffer=chunk)
    print("녹음 중...")

    frames = []

    # 설정된 시간 동안 마이크로부터 오디오 데이터 녹음
    for i in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print("녹음 완료.")

    # 스트림 정지 및 닫기
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 녹음된 오디오를 WAV 파일로 저장
    waveFile = wave.open(filename, 'wb')
    waveFile.setnchannels(channels)
    waveFile.setsampwidth(audio.get_sample_size(format))
    waveFile.setframerate(rate)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    return filename

# 예시 사용법
recorded_file = record("file.wav", 5)
print(f"녹음된 파일: {recorded_file}")

model = whisper.load_model("small")
result = model.transcribe("file.wav")
print(result["text"])