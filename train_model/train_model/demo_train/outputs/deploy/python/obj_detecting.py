import openvino as ov
import cv2
import numpy as np
import ipywidgets as widgets
import os
import time

class ObjectDetection:
    def __init__(self, model_xml, model_bin, device="AUTO"):
        # 모델 파일의 경로와 사용할 디바이스를 입력으로 받아 초기화합니다.
        self.model_xml = model_xml
        self.model_bin = model_bin

        self.core = ov.Core()
        self.device = widgets.Dropdown(
            options=self.core.available_devices + ["AUTO"],
            value='AUTO',
            description='Device:',
            disabled=False,
        )
        # 모델을 로드하고, 실행할 디바이스에 맞게 최적화합니다.
        self.model = self.core.read_model(model=self.model_xml)
        self.compiled_model = self.core.compile_model(
            model=self.model, device_name=self.device.value)
        # 모델의 입력과 출력 키를 가져옵니다.
        self.input_keys = self.compiled_model.input(0)
        self.boxes_output_keys = self.compiled_model.output(0)
        self.labels_output_keys = self.compiled_model.output(1)
        # 이미지의 높이와 너비를 설정합니다.
        self.height = 736
        self.width = 992

    def preprocess_image(self, image):
        # 이미지를 모델 입력에 맞게 전처리합니다.
        resized_image = cv2.resize(image, (self.width, self.height))
        input_image = np.expand_dims(resized_image.transpose(2, 0, 1), 0)
        return input_image

    def detect_object(self, processed_image):
        # 전처리된 이미지에서 손을 감지합니다.
        results = self.compiled_model([processed_image])
        boxes = results[self.boxes_output_keys]
        labels = results[self.labels_output_keys]

        # 신뢰도 점수를 기준으로 가장 높은 값을 가진 객체를 찾습니다.
        max_confidence_index = np.argmax(boxes[0, :, 4])
        max_confidence_box = boxes[0, max_confidence_index]
        max_confidence_label = labels[0, max_confidence_index]
        return max_confidence_box, max_confidence_label

    def run(self, image):
        # 이미지를 입력받아 감지된 물체를 리턴합니다.
        processed_image = self.preprocess_image(image)
        box, label = self.detect_object(processed_image)
        # 레이블에 해당하는 동작 이름을 가져옵니다.
        object_naem = ['person', 'book']
        object = object_naem[label]
        confidence = box[4]*100
        return object, confidence, box


# 사용예제
object_detector = ObjectDetection(model_xml='../model/model.xml', \
                                  model_bin='../model/model.bin')

cap = cv2.VideoCapture(4)

image_counter = 0
max_images = 30
book_poto_time = time.time()
person_poto_time = time.time()

while True:
    ret, frame = cap.read()
    current_time = time.time()
    if not ret:
        print("입력이 없습니다.")
        break
    # 감지된 물체의 레이블과 신뢰도를 출력합니다.
    label, confidence, box = object_detector.run(frame)
    # if confidence > 50:
    #     print(label, confidence)
    # 웹캠의 프레임을 화면에 출력합니다.

    cv2.imshow('Webcam', frame)

    # 라벨이 "book"인 경우
    if label == "book":
        save_path = './crop_images'  # 이미지 저장 경로 설정
        # 디렉토리가 없으면 생성
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # 바운딩 박스 좌표
        x_min, y_min, x_max, y_max = map(int, box[:4])

        # 바운딩 박스에 해당하는 부분만 자르기
        cropped_image = frame[y_min:y_max, x_min:x_max]

        # 이미지가 비어 있지 않은 경우에만 저장
        if not cropped_image.size == 0 and current_time-book_poto_time > 2:
            # 이미지를 저장
            cv2.imwrite(
                f"{save_path}/book_image_{image_counter}.jpg", cropped_image)
            print(image_counter)
            image_counter += 1

            book_poto_time = time.time()

            # 저장할 이미지의 최대 개수에 도달하면 프로그램 종료
            if image_counter >= max_images:
                print(f"{max_images}장의 이미지를 저장하였습니다. 프로그램을 종료합니다.")
                break


    # 라벨이 "person"인 경우
    elif label == "person":
        save_path = './checkout'  # 이미지 저장 경로 설정
        # 디렉토리가 없으면 생성
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # 바운딩 박스 좌표
        x_min, y_min, x_max, y_max = map(int, box[:4])

        # 바운딩 박스에 해당하는 부분만 자르기
        cropped_image = frame[y_min:y_max, x_min:x_max]

        # 이미지가 비어 있지 않은 경우에만 저장
        if not cropped_image.size == 0 and current_time-person_poto_time > 2:
            # 이미지를 저장
            cv2.imwrite(
                f"{save_path}/person_image_{image_counter}.jpg", cropped_image)
            print(image_counter)
            image_counter += 1

            person_poto_time = time.time()

            # 저장할 이미지의 최대 개수에 도달하면 프로그램 종료
            if image_counter >= max_images:
                print(f"{max_images}장의 이미지를 저장하였습니다. 프로그램을 종료합니다.")
                break


    # 'q' 키를 누르면 종료합니다.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# 웹캠을 해제하고 모든 창을 닫습니다.
cap.release
cv2.destroyAllWindows()
