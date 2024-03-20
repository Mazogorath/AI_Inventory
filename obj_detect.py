import openvino as ov
import cv2
import numpy as np
import ipywidgets as widgets
import os
import time

# ID: "https://192.168.0.136:8080/stream"


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
        self.model = self.core.read_model(model=self.model_xml)
        self.compiled_model = self.core.compile_model(
            model=self.model, device_name=self.device.value)
        self.input_keys = self.compiled_model.input(0)
        self.boxes_output_keys = self.compiled_model.output(0)
        self.labels_output_keys = self.compiled_model.output(1)

        self.height = 640
        self.width = 640

    def preprocess_image(self, image):
        resized_image = cv2.resize(image, (self.width, self.height))
        input_image = np.expand_dims(resized_image.transpose(2, 0, 1), 0)
        return input_image

    def detect_objects(self, processed_image):
        results = self.compiled_model([processed_image])
        boxes = results[self.boxes_output_keys]
        labels = results[self.labels_output_keys]
        return boxes, labels

    def run(self, image):
        processed_image = self.preprocess_image(image)
        boxes, labels = self.detect_objects(processed_image)
        return boxes, labels


def Object_capture(ID):
    object_detector = ObjectDetection(model_xml='./models/model.xml',
                                      model_bin='./models/model.bin')

    cap = cv2.VideoCapture(ID)

    book_image_counter = 0
    person_image_counter = 0
    book_max_images = 201
    person_max_images = 201
    # book_photo_time = time.time()
    # person_photo_time = time.time()

    # while True:
    for i in range(0, 50):
        ret, frame = cap.read()
        if not ret:
            print("입력이 없습니다.")
            break

        cv2.imshow("frame", frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # while True:
    # ret, frame = cap.read()
    # current_time = time.time()

        # break

    boxes, labels = object_detector.run(frame)

    # 2번 imshow되어 주석처리 while문 사용 시 필요 구문으로 삭제 안함
    # cv2.imshow('Webcam', frame)
    scrinshot = []

    for i, (box, label) in enumerate(zip(boxes[0], labels[0])):
        confidence = box[4]
        # print(confidence)
        if confidence < 0.89:
            continue

        if label == 1:
            color = (0, 255, 0)
        elif label == 0:
            color = (255, 0, 0)
        else:
            continue

        x_min, y_min, x_max, y_max = map(int, box[:4])

        # 좌표 보정
        x_min = max(0, x_min)
        y_min = max(0, y_min)
        x_max = min(frame.shape[1], x_max)
        y_max = min(frame.shape[0], y_max)

        # 바운딩 박스 및 confidence 생성 구문 추가
        # cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        # cv2.putText(frame, f'Confidence: {confidence}', (x_min, y_min), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imwrite("check.jpg", frame)

        cropped_image = frame[y_min:y_max, x_min:x_max]
        # print(confidence)

        scrinshot.append((cropped_image, label))  # 이미지와 레이블을 튜플로 저장

    # scrinshot 배열의 원소를 모두 저장하는 부분
    for cropped_image, label in scrinshot:
        # print("Label:", label)
        # print(len(scrinshot))
        if not cropped_image.size == 0:
            # 검사용 코드 추가
            # print(f"Bounding Box Coordinates: {x_min}, {y_min}, {x_max}, {y_max}")
            # print(f"cropped_image size: {cropped_image.size}")
            save_path = './crop_images' if label == 1 else './checkout'
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            if label == 1:
                if book_image_counter >= book_max_images:
                    print(
                        f"{book_max_images}장의 이미지를 저장하였습니다. 프로그램을 종료합니다.")
                    # cap.release()
                    cv2.destroyAllWindows()
                    print(book_image_counter)
                    return len(scrinshot)
                cv2.imwrite(
                    f"{save_path}/book_image_{book_image_counter}.jpg", cropped_image)
                # 카메라 위치 조정확인을 위한 구문
                # cv2.imwrite(f"{save_path}/check.jpg", frame)
                # book_photo_time = time.time()
                # print(confidence)
                # print(scrinshot)
                book_image_counter += 1
                print("book", book_image_counter)

            elif label == 0:
                if person_image_counter >= person_max_images:
                    print(
                        f"{person_max_images}장의 이미지를 저장하였습니다. 프로그램을 종료합니다.")
                    # cap.release()
                    cv2.destroyAllWindows()
                    return

                cv2.imwrite(
                    f"{save_path}/person_image_{person_image_counter}.jpg", cropped_image)
                # 카메라 위치 조정확인을 위한 구문
                # cv2.imwrite(f"{save_path}/check.jpg", frame)
                # person_photo_time = time.time()
                person_image_counter += 1
                print("person", person_image_counter)
                print(confidence)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break


# url = "http://192.168.0.136:8080/stream"
# Object_capture(url)
