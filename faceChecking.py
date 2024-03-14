import os
import cv2
import platform
import numpy as np
import datetime
from openvino.runtime import Core

# Basic Paths
MODEL_BASE_PATH: str = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "models")
DETECT_MODEL_PATH: str = os.path.join(MODEL_BASE_PATH, "detect_model.xml")
DETECT_MODEL_BIN_PATH: str = os.path.join(MODEL_BASE_PATH, "detect_model.bin")
RECOG_MODEL_PATH_1: str = os.path.join(MODEL_BASE_PATH, "recog_model.xml")
RECOG_MODEL_BIN_PATH_1: str = os.path.join(MODEL_BASE_PATH, "recog_model.bin")
RECOG_MODEL_PATH_2: str = os.path.join(
    MODEL_BASE_PATH, "arcfaceresnet100.onnx")
IMAGE_PATH: str = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "images")

# Camera Setting
ID: int = 10
CAM_WIDTH: int = 640
CAM_HEIGHT: int = 360
FPS: int = 60

# Make Lists with Image Files
raw_list = os.listdir(IMAGE_PATH)
file_list = []
employees = []
reference_embeddings = []
cs = []
for i in raw_list:
    filename = os.path.splitext(i)[1]
    if filename == '.jpg' or filename == '.jpeg' or filename == '.png':
        file_list.append(i)
        employees.append(os.path.splitext(i)[0])

del raw_list

# Clahe Filter Preset
clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(5, 5))


# Make Image/Frame into Required Size and Channels for Inference
def preprocess(image: np.ndarray, width: int, height: int, model_name: str = "arcface") -> np.ndarray:

    if model_name == "facenet":
        image = cv2.resize(src=image, dsize=(width, height),
                           interpolation=cv2.INTER_AREA)
    else:
        image = cv2.resize(src=image, dsize=(width, height),
                           interpolation=cv2.INTER_AREA).transpose(2, 0, 1)

    return np.expand_dims(image, axis=0)


# Compute the cosine similarity between two vectors
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:

    return np.dot(a, b.reshape(-1, 1)) / (np.linalg.norm(a) * np.linalg.norm(b))


# Setup the OpenVino Model
def setup(target: str, model_path: str, bin_path: str) -> tuple:

    ie = Core()
    model = ie.read_model(model=model_path, weights=bin_path)
    model = ie.compile_model(model=model, device_name=target)

    input_layer = next(iter(model.inputs))
    output_layer = next(iter(model.outputs))

    return model, input_layer, output_layer, \
        (input_layer.shape[0], input_layer.shape[1],
         input_layer.shape[2], input_layer.shape[3])


# Detect Faces in the Image
def detect_faces(
    model,
    output_layer,
    image: np.ndarray,
    w: int,
    h: int,
    threshold: float = 0.9,
) -> tuple:

    result = model(inputs=[image])[output_layer].squeeze()

    label_indexes: list = []
    probs: list = []
    boxes: list = []

    if result[0][0] == -1:
        return 0, None, None
    else:
        for i in range(result.shape[0]):
            if result[i][0] == -1:
                break
            elif result[i][2] > threshold:
                label_indexes.append(int(result[i][1]))
                probs.append(result[i][2])
                boxes.append([int(result[i][3] * w),
                              int(result[i][4] * h),
                              int(result[i][5] * w),
                              int(result[i][6] * h)])
            else:
                pass
    label_indexes, probs, boxes
    return label_indexes, probs, boxes


# Make a List of Face of Employees Based on Images
def processPictures(target="CPU", model="facenet"):

    count = -1
    for file in file_list:
        count += 1
        # Apply CLAHE to Images
        image = cv2.imread(os.path.join(
            IMAGE_PATH, file), cv2.IMREAD_COLOR)
        for i in range(3):
            image[:, :, i] = clahe.apply(image[:, :, i])
        temp_image = image.copy()
        h, w, _ = image.shape

        # Initialize Facial Detection Model
        d_model, _, d_output_layer, (_, _, d_H, d_W) = setup(
            target, DETECT_MODEL_PATH, DETECT_MODEL_BIN_PATH)

        # Initialize Facial Recognition Model (Facial Embeddings)
        if model == "facenet":
            r_model, _, r_output_layer, (_, r_H, r_W, _) = setup(
                target, RECOG_MODEL_PATH_1, RECOG_MODEL_BIN_PATH_1)
        elif model == "arcface":
            r_model, _, r_output_layer, (_, _, r_H, r_W) = setup(
                target, RECOG_MODEL_PATH_2)

        # Preprocess Image and Detect Faces
        image = preprocess(image, d_W, d_H)
        _, _, boxes = detect_faces(d_model, d_output_layer, image, w, h)

        # Preprocess Face ROI Image and Get Embeddings
        face_image = preprocess(
            temp_image[boxes[0][1]:boxes[0][3], boxes[0][0]:boxes[0][2], :], r_W, r_H, model)
        reference_embeddings.append(
            r_model(inputs=[face_image])[r_output_layer])

        del temp_image, boxes, image

        # Append Cosine Similarity Point of Face into the List
        cs.append(cosine_similarity(
            reference_embeddings[count], reference_embeddings[count])[0][0])

    return d_model, d_output_layer, d_H, d_W, r_model, r_output_layer, r_H, r_W


def faceCheckings(model="facenet"):

    # Process Employee's pictures into reference
    d_model, d_output_layer, d_H, d_W, r_model, r_output_layer, r_H, r_W = processPictures()

    # Initialize Video Capture Object
    if platform.system() != "Windows":
        cap = cv2.VideoCapture(ID)
    else:
        cap = cv2.VideoCapture(ID, cv2.CAP_DSHOW)

    # Set parameters of capture object
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)

    # Read data from Video Capture Object
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Make a Copy for Processing and Displaying
        temp_frame = frame.copy()
        disp_frame = frame.copy()

        # Apply CLAHE
        for i in range(3):
            frame[:, :, i] = clahe.apply(frame[:, :, i])
            temp_frame[:, :, i] = clahe.apply(temp_frame[:, :, i])

        # Preprocess Frame and Detect Faces
        frame = preprocess(frame, d_W, d_H)
        _, _, boxes = detect_faces(
            d_model, d_output_layer, frame, CAM_WIDTH, CAM_HEIGHT)

        # Preprocess Face ROI Frame and Get Embeddings
        for box in boxes:
            face_frame = temp_frame[box[1]:box[3], box[0]:box[2], :]

            # Go Back to Starting Point When There's Nothing
            if face_frame.shape[0] < 16 or face_frame.shape[1] < 16:
                cv2.putText(disp_frame, "ROI to small to detect", org=(
                    25, 75), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=1, color=(0, 0, 255))
                continue

            # Compute Cosine Similarity between Embeddings
            face_frame = preprocess(face_frame, r_W, r_H, model)
            embeddings = r_model(inputs=[face_frame])[r_output_layer]
            klist = []
            for j in reference_embeddings:
                klist.append(cosine_similarity(j, embeddings)[0][0])

            # Highlight Employee's Face
            max_idx = np.argmax(klist)
            if klist[max_idx] > 0.5:
                print(klist[max_idx])
                pt1 = (box[0], box[1])
                pt2 = (box[2], box[3])
                cv2.rectangle(disp_frame, pt1, pt2, color=(0, 255, 0))
                cv2.putText(disp_frame, f"{employees[max_idx]}", org=(
                    box[0] + 5, box[1] + 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=1, color=(0, 255, 0))
                if klist[max_idx] > 0.65:
                    now = datetime.datetime.now()
                    cv2.imwrite(
                        f"./Pictures/{now}_{employees[max_idx]}.jpg", disp_frame)
                    cv2.destroyAllWindows()
                    return f"{employees[max_idx]}", disp_frame

            # Show frame with boxes
            cv2.imshow("Feed", disp_frame)

        # Press 'q' to Quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the Video Capture Object
    cap.release()

    # Destroy all cv2 Windows
    cv2.destroyWindow("Feed")


faceCheckings()
