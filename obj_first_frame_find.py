import openvino as ov
import cv2
import numpy as np
import ipywidgets as widgets
import os
import time

class ObjectDetection:
    def __init__(self, model_xml, model_bin, device="AUTO"):
        self.model_xml = model_xml
        self.model_bin = model_bin

        self.core = ov.Core()
        self.device = widgets.Dropdown(
            options=self.core.available_devices + ["AUTO"],
            value='AUTO',
            description='Device:',
            disabled=False,
        )
        self.model = self.core.read_model(model=model_xml, weights=model_bin)
        self.compiled_model = self.core.compile_model(model=self.model, device_name=device)
        self.input_layer = next(iter(self.compiled_model.inputs))
        self.output_layer = next(iter(self.compiled_model.outputs))

    def start_video_capture(self):
        # 카메라 초기화
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("Could not open video device")

        # 3초 대기
        time.sleep(3)

        # 첫 프레임 캡처 및 저장
        ret, frame = self.cap.read()
        if ret:
            cv2.imwrite('first_frame.jpg', frame)
            print("First frame captured and saved.")
        else:
            print("Failed to capture frame.")

    def detect_objects_in_frame(self, frame_path):
        # 저장된 프레임을 불러옴
        frame = cv2.imread(frame_path)
        # 프레임 전처리
        input_image = cv2.resize(frame, (self.input_layer.shape[2], self.input_layer.shape[3]))
        input_image = input_image.transpose((2, 0, 1))  # Change data layout from HWC to CHW
        input_image = np.expand_dims(input_image, 0)

        # 객체 탐지 실행
        results = self.compiled_model.infer(inputs={self.input_layer.any_name: input_image})
        # 결과 처리 및 출력 (여기에서는 간단히 결과를 출력만 합니다. 실제로는 탐지된 객체에 대한 처리를 구현해야 합니다.)
        print("Detection results:", results)

# 객체 탐지 모델 초기화 (모델 파일 경로는 실제 환경에 맞게 수정해야 합니다.)
object_detection = ObjectDetection("/home/busan/inventory/AI_Inventory/train_model/model/model.xml", "/home/busan/inventory/AI_Inventory/train_model/model/model.bin")
# 비디오 캡처 시작
object_detection.start_video_capture()
# 첫 프레임에서 객체 탐지 실행
object_detection.detect_objects_in_frame("first_frame.jpg")
