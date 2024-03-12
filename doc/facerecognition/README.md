## Update
2024.03.07 여러 얼굴의 동시 검출 기능 추가, Recognition 모델 추가, 프로그램 모듈화
2024.03.08 입장/퇴장할 때마다 리스트와 연동하여 중복 인식 방지, 음성 인식과 연동하여 신원 확인 시 메시지 표시

# 얼굴 탐지 및 인식 프로그램

## 파일
    faceChecking.py = 얼굴 탐지/인식 기능
    ComingIn.py = 입구 카메라용 프로그램
    ComingOut.py = 출구 카메라용 프로그램
    InandOut.py = 스레딩으로 출입 모두 구현 시도, buggy
    Whisper.py = 최영중님의 음성 인식 프로그램 (version = 0308)
    

## 함수
    preprocess() = 이미지의 사이즈와 차원 순서 변경
    cosine_similarity() = 두 벡터(얼굴)의 유사한 정도를 반환
    setup() = OpenVino 모델 셋업
    processPictures() = Images 폴더 내의 인물 사진 분석
    detect_faces() = 얼굴 검출
    faceCheckings() = main 함수, 사진과 영상 비교

## 흐름
    1. 데이터베이스에 등록된 인물 사진 분석
    	(1) 명암 대비 향상 (CLAHE 알고리즘)
    	(2) 사진에서 얼굴 검출 = detect_faces()
    	(3) 얼굴의 특징 분석, 벡터로 반환 = processPictures()
    2. 실시간 영상과 비교
    	(1) 영상 전처리 = preprocess() + 기타
    	(2) 영상에서 얼굴 검출 = detect_faces()
    	(3) 얼굴의 특징 분석, 벡터로 반환
    	(4) 사진과 영상 비교 = cosine_similarity()
    	(5) 비교 결과가 일정 값 이상이면 동일인으로 간주
    	
    	
## 폴더
images = 직원 등록용 사진 저장 폴더
Pictures = 사람이 인식된 경우 사진 저장
