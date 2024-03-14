## Update
2024.03.07 마이크로 음성 입력 후 Text 출력 기본틀 생성   
2024.03.08 DB 생성 후 Product 단어 검출 시 음성 출력   
2024.03.14 GUI 구현 이후 INPUT VOICE 화면 출력 예정   

# Whisper Mic
Whisper Mic은 OpenAI의 자동 음성 인식(Automatic Speech Recognition, ASR) 기술, Whisper를 기반으로 하는 오픈 소스 프로젝트입니다.   
마이크를 사용하여 실시간으로 음성을 텍스트로 변환할 수 있습니다.

# 사용 가능한 모델과 언어
| Size   | Parameters | English-only Model | Multilingual Model | Required VRAM | Relative Speed |
|--------|------------|--------------------|--------------------|---------------|----------------|
| Tiny   | 39 M       | tiny.en            | tiny               | ~1 GB         | ~32x           |
| Base   | 74 M       | base.en            | base               | ~1 GB         | ~16x           |
| Small  | 244 M      | small.en           | small              | ~2 GB         | ~6x            |
| Medium | 769 M      | medium.en          | medium             | ~5 GB         | ~2x            |
| Large  | 1550 M     | N/A                | large              | ~10 GB        | 1x             |

## 가상 환경 생성
python -m venv venv

## 가상 환경 활성화
**Windows**
```bash
.\venv\Scripts\activate
```
**MacOS/Linux**
```bash
source venv/bin/activate
```

## Whisper Mic 설치
```python
pip install whisper-mic
```

## 예제 코드
```python
from whisper_mic import WhisperMic

mic = WhisperMic()
result = mic.listen()
print(result)
```

## 종속성 문제 발생시
```bash
sudo apt install portaudio19-dev python3-pyaudio
```

## 출처
https://github.com/mallorbc/whisper_mic
