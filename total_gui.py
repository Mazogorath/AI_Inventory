import cv2
import sys
import time
import serial
import speech_recognition as sr
import test_Whisper

from PySide6.QtCore import Qt, QThread, QTimer, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QPushButton, QWidget, QLineEdit

from faceChecking import faceCheckings
# from MainProgram import UID_check
from obj_detect import Object_capture
from person_detection import person_detect
import test_Whisper
camera_id = {'A': 4, 'B': 'http://192.168.0.32:5000/video', 'C': 4, 'D': 'http://192.168.0.32:5000/video'}
carried_out = {}
main_cam_id = 12


class FaceRecognitionThread(QThread):
    update_signal = Signal(str, QImage)

    def run(self):
        # 예제를 위한 가상의 faceCheckings 함수 호출
        name, frame = faceCheckings(mode="Video", ID=main_cam_id)
        if frame is not None:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            qt_image = QImage(
                rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
            self.update_signal.emit(name, qt_image)


class GUI1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initFaceRecognition()

    def initUI(self):
        self.setWindowTitle('PySide6 UI with Camera')
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.camera_label = QLabel()
        layout.addWidget(self.camera_label)

        self.message_label = QLabel()
        layout.addWidget(self.message_label)

        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.go_next_screen)
        layout.addWidget(self.next_button)

        self.exit_button = QPushButton('Exit')
        self.exit_button.clicked.connect(self.exit_program)
        layout.addWidget(self.exit_button)

    def initFaceRecognition(self):
        self.face_recognition_thread = FaceRecognitionThread()
        self.face_recognition_thread.update_signal.connect(self.update_frame)
        self.face_recognition_thread.start()

    def update_frame(self, name, image):
        pixmap = QPixmap.fromImage(image)
        self.camera_label.setPixmap(pixmap)
        self.message_label.setText(f"{name}님 안녕하세요. 무엇을 도와드릴까요?")
        self.next_button.setEnabled(True)

    def go_next_screen(self):
        self.close()
        self.next_window = GUI2()
        self.next_window.show()

    def exit_program(self):
        QApplication.quit()


class GUI2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("GUI with PySide6")
        self.setGeometry(100, 100, 1000, 600)

        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Image label container
        image_container = QWidget()
        image_layout = QHBoxLayout(image_container)
        image_container.setLayout(image_layout)
        layout.addWidget(image_container, alignment=Qt.AlignCenter)

        # Create four image labels
        self.image_labels = [QLabel() for _ in range(4)]
        for label in self.image_labels:
            label.setFixedSize(320, 250)  # Adjust size as needed
            image_layout.addWidget(label)

        # Text labels
        self.text_label_1 = QLabel()
        layout.addWidget(self.text_label_1, alignment=Qt.AlignCenter)

        self.text_label_2 = QLabel()
        self.text_label_2.setWordWrap(True)
        layout.addWidget(self.text_label_2, alignment=Qt.AlignCenter)

        # Buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        whisper_button = QPushButton("Check")
        whisper_button.clicked.connect(self.update_text)
        button_layout.addWidget(whisper_button, alignment=Qt.AlignCenter)

        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.go_next_screen3)
        button_layout.addWidget(self.next_button)

        prev_button = QPushButton('Prev')
        prev_button.clicked.connect(self.go_prev_screen)
        button_layout.addWidget(prev_button)

    def show_image(self):
        image_paths = [
            "./crop_image/A/check.jpg",
            "./crop_image/B/check.jpg",
            "./crop_image/C/check.jpg",
            "./crop_image/D/check.jpg",
        ]

        for i, path in enumerate(image_paths):
            print(f"i: {i}, path: {path}")
            pixmap = QPixmap(path)
            pixmap = pixmap.scaled(
                300, 250, Qt.AspectRatioMode.KeepAspectRatio)
            self.image_labels[i].setPixmap(pixmap)

    def update_text(self):
        # self.show_image()
        print("update_text")
        camera_data = camera_id
        screenshot_counts = {}  # Dictionary to store screenshot counts for each camera ID

        # Capture screenshots and store counts
        for key, value in camera_data.items():
            screenshot_counts[key] = Object_capture(value, key)
            time.sleep(1)

        # Update text label 1
        total_count = sum(screenshot_counts.values())
        self.text_label_1.setText(
            f"총 스크린샷 개수는 {total_count} 개 입니다."
        )

        # Update image labels and text label 2 (assuming details from recognized text)
        # List to store details for each screenshot (if applicable)
        details_list = []
        for i, (key, count) in enumerate(screenshot_counts.items()):
            #self.show_image()
            print(f"2nd i = {i}")
            # Or set a placeholder image
            self.image_labels[i].setText(f"{key}위치 스크린샷")

            # Replace this with your logic to retrieve details based on recognized text
            details = None  # Placeholder
            details_list.append(details)
        
        self.show_image()

        details_text = "\n".join(
            details_list) if details_list else "상품 정보를 가져오지 못했습니다."
        self.text_label_2.setText(details_text)

    def go_next_screen3(self):
        self.close()
        self.next_window = GUI3()
        self.next_window.show()

    def go_prev_screen(self):
        self.close()
        self.next_window = GUI1()


class GUI3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Detection")
        self.setGeometry(100, 100, 800, 800)
        self.currentImageIndex = 0
        self.imagePaths = [
            "./location/map.png",
            "./location/map_a.png",
            "./location/map_b.png",
            "./location/map_c.png",
            "./location/map_d.png"
        ]
        self.initUI()

    def initUI(self):
        # 메인 위젯 설정
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        # 전체 레이아웃 설정
        self.mainLayout = QVBoxLayout()
        self.centralWidget.setLayout(self.mainLayout)

        # 타이틀 바 버튼 레이아웃 설정
        self.titleBarLayout = QHBoxLayout()
        self.buttonNext = QPushButton("음성입력", self)
        self.buttonNext.clicked.connect(self.listen_to_speech)
        self.titleBarLayout.addStretch()  # 버튼 사이의 공간을 추가합니다.
        self.titleBarLayout.addWidget(self.buttonNext)
        self.mainLayout.addLayout(self.titleBarLayout)
        # # 제품 번호 입력 필드와 세부 정보 조회 버튼 레이아웃 설정
        # self.productInputLayout = QHBoxLayout()
        # self.productNumberInput = QLineEdit(self)
        # self.productNumberInput.setPlaceholderText("제품 번호 입력")
        # self.productInfoButton = QPushButton("세부 정보 조회", self)
        # self.productInfoButton.clicked.connect(self.display_selected_product_details)
        
        # self.productInputLayout.addWidget(self.productNumberInput)
        # self.productInputLayout.addWidget(self.productInfoButton)
        # self.mainLayout.addLayout(self.productInputLayout)

        # Navigation buttons
        # Create a layout for navigation buttons.
        self.navButtonLayout = QHBoxLayout()
        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.go_next_screen3)
        self.navButtonLayout.addWidget(self.next_button)

        prev_button = QPushButton('Prev')
        prev_button.clicked.connect(self.go_prev_screen)
        self.navButtonLayout.addWidget(prev_button)
        # Add navigation buttons layout to the main layout.
        self.mainLayout.addLayout(self.navButtonLayout)

        # 'View Location' 이미지 뷰어 설정
        self.imageView = QLabel(self)
        self.imageView.setFixedSize(760, 560)
        self.imageView.setAlignment(Qt.AlignCenter)
        self.imageView.setStyleSheet("border: 1px solid blue;")
        self.mainLayout.addWidget(self.imageView)

        # 'Log Text' 텍스트 에디터 설정
        self.logTextEdit = QTextEdit(self)
        self.logTextEdit.setFixedSize(760, 100)
        self.logTextEdit.setReadOnly(True)
        self.mainLayout.addWidget(self.logTextEdit)
        self.logTextEdit.setText("찾으시는 제품을 말하세요.")
        # 이미지 표시하기
        self.displayImage(self.imagePaths[self.currentImageIndex])

    def display_selected_product_details(self):
        product_index = int(self.productNumberInput.text()) - 1  # 사용자 입력은 1부터 시작하므로 인덱스에 맞게 조정
        self.selected_product_details(product_index)

    def displayNextImage(self):
        # 다음 이미지를 표시하는 함수
        self.currentImageIndex += 1
        if self.currentImageIndex >= len(self.imagePaths):
            self.currentImageIndex = 0  # 리스트의 끝에 도달하면 다시 처음으로
        self.displayImage(self.imagePaths[self.currentImageIndex])

    def displayImage(self, path):
        # 이미지 로드 및 레이블에 표시
        pixmap = QPixmap(path)
        self.imageView.setPixmap(pixmap.scaled(
            self.imageView.width(), self.imageView.height(), Qt.KeepAspectRatio))
        self.imageView.show()  # 이미지 레이블을 다시 그립니다.

    def listen_to_speech(self):
        duration = 3
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=duration)
            print("찾으시는 제품을 말하세요.")
            audio_data = recognizer.listen(source)
            try:
                print("Loading")
                text = recognizer.recognize_google(audio_data, language='ko-KR')
                print(f"인식된 텍스트: {text}")
                self.logTextEdit.setText(f"인식된 텍스트: {text}")

                details, response = self.find_product_info(text, test_Whisper.products)
                if details:
                    self.logTextEdit.setText(response)
                    # 사용자가 제품을 선택할 수 있도록 안내 메시지 추가
                    self.logTextEdit.append("\n제품 번호를 입력하여 세부 정보를 조회하세요.")
                    self.current_product_details = details  # 현재 검색 결과 저장
                    # location = self.extract_location(details)
                    print(self.extract_location(details))
                    # self.logTextEdit.append(f"위치: {location}")
                    # self.displayImage(self.imagePaths[self.currentImageIndex])
                else:
                    self.logTextEdit.setText(response)
                    print("success")
                
                # location = self.extract_location(details)
                # self.logTextEdit.append(f"위치: {location}")
                # self.displayImage(self.imagePaths[self.currentImageIndex])
            except sr.UnknownValueError:
                self.logTextEdit.setText("다시 말씀해 주시겠습니까?.")
            except sr.RequestError as e:
                self.logTextEdit.setText(f"에러: {e}")

    def selected_product_details(self, product_index):
    # 제품 인덱스를 사용하여 해당 제품의 세부 정보를 표시
        if 0 <= product_index < len(self.current_product_details):
            detail = self.current_product_details[product_index]
            self.logTextEdit.setText(detail)
        else:
            self.logTextEdit.setText("잘못된 제품 번호입니다. 다시 시도해 주세요.")
    
    def find_product_info(self, recognized_text, products):
        keyword = recognized_text.split()[0].lower()
        results = [product for product in products if keyword in product["제품 이름"].lower()]

        if results:
            response = "\n".join(f"{idx+1}: {product['제품 이름']}" for idx, product in enumerate(results))
            details = [f"{product['제품 이름']}, 수량: {product['수량']}, 위치: {product['위치']}, 가격: {product['가격']}, 저자: {product['저자']}, UID: {product['UID']}" for product in results]
            return details, response
        else:
            response = "인식된 키워드에 해당하는 제품을 찾을 수 없습니다."
            return None, response

    def extract_location(self, product_info):
            # 위치 정보를 추출하는 로직 변경
            location = None
            for item in product_info:
                if "위치: " in item:
                    location_start_index = item.find("위치: ") + len("위치: ")
                    # 쉼표로 구분된 다음 세부 정보의 시작 지점을 찾습니다.
                    comma_index = item.find(",", location_start_index)
                    # 쉼표가 발견되면, 위치 시작 지점부터 쉼표 이전까지의 문자열을 추출합니다.
                    if comma_index != -1:
                        location = item[location_start_index:comma_index]
            
            if location is not None:
                # 위치에 따라 이미지 맵에서 이미지 경로를 찾아 화면에 표시
                image_map = {
                    'A': self.imagePaths[1],
                    'B': self.imagePaths[2],
                    'C': self.imagePaths[3],
                    'D': self.imagePaths[4],
                }
                if location in image_map:
                    self.displayImage(image_map[location])
                    location_message = f"찾으시는 제품은 {location} 위치에 있습니다."
                    self.logTextEdit.append(location_message)  # 텍스트 로그에 메시지 추가
                else:
                    self.logTextEdit.append("해당 위치의 이미지가 없습니다.")
            else:
                self.logTextEdit.append("위치 정보를 찾을 수 없습니다.")

            # 리스트인 product_info를 문자열로 변환하여 로그에 추가
            details_message = ', '.join(product_info)
            self.logTextEdit.append(details_message)

    def go_next_screen3(self):
        self.close()
        self.next_window = GUI4()
        self.next_window.show()

    def go_prev_screen(self):
        self.close()
        self.next_window = GUI2()
        self.next_window.show()


class GUI4(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('PySide6 UI with Camera')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.camera_label = QLabel()
        layout.addWidget(self.camera_label)

        self.message_label = QLabel()
        layout.addWidget(self.message_label)

        prev_button = QPushButton('Return')
        prev_button.clicked.connect(self.go_prev_screen)
        layout.addWidget(prev_button)

        self.exit_button = QPushButton('Exit')
        self.exit_button.clicked.connect(self.exit_program)
        layout.addWidget(self.exit_button)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # self.carried_out = {}  # 반출된 UID 저장

        # 시리얼 포트 설정
        self.serial_port = '/dev/ttyACM0'
        self.ser = serial.Serial(self.serial_port, baudrate=9600, timeout=1)

        # 마지막으로 찍힌 UID와 시각
        self.last_uid = None
        self.last_uid_time = time.time()

    def read_data(self):
        data = self.ser.readline().decode('utf-8').rstrip()
        if len(data) == 8:
            # 동일한 UID는 5초 지나야 다시 찍을 수 있음
            if data == self.last_uid and time.time() - self.last_uid_time < 5:
                print("I hate this")
                return None 
            return data

    def update_frame(self):
        uid_data = self.read_data()
        if uid_data:
            for product in test_Whisper.products:
                if uid_data == product["UID"]:
                    Pname = product["제품 이름"]
                    break
            else:
                self.message_label.setText(f"{uid_data}에 해당하는 상품 없음")

            print("UID 확인 완료")
            # 마지막으로 찍힌 UID와 시각 저장
            self.last_uid = uid_data
            self.last_uid_time = time.time()

            # 얼굴 인식, 사람 인식
            name, frame = faceCheckings(mode="Video", ID=main_cam_id)
            # person_detect()

            if frame is not None:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                qt_image = QImage(
                    rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                self.camera_label.setPixmap(pixmap)

# q쓰레드 선언
# init 으로 이미지를 쏴줘라
# 받는 업데이트 시그널을 이미지를 써야댄다.

            if name is not None:
                if uid_data not in carried_out:
                    carried_out[uid_data] = name
                    print(carried_out)
                    self.message_label.setText(f"{name},{Pname} 반출 등록")
                else:
                    carried_out.pop(uid_data)
                    print(carried_out)
                    self.message_label.setText(f"{name},{Pname} 반납 확인")
                self.face_recognized = True
        else:
            pass

    def go_prev_screen(self):
        self.close()
        self.next_window = GUI1()
        self.next_window.show()

    def exit_program(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = GUI1()
    widget.show()
    sys.exit(app.exec_())
