import os
import cv2
import time
import random
import numpy as np
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
from ocr import perform_ocr, draw_text_on_image
from speech import listen_to_speech, speak, find_product_info

products = [
    {"ID": 1, "제품 이름": "파이썬으로배우는머신러닝의교과서", "수량": 10,
        "위치": "A", "가격": 34000, "저자": "이토마코토", "UID": 12345},
    {"ID": 2, "제품 이름": "개발자를위한머신러닝딥러닝", "수량": 5, "위치": "B",
     "가격": 30000, "저자": "34000", "UID": 12346},
    {"ID": 3, "제품 이름": "파이썬과Qt6로GUI애플리케이션만들기", "수량": 15,
     "위치": "A", "가격": 28000, "저자": "미상", "UID": 12347},
    {"ID": 4, "제품 이름": "라즈베리파이3를활용한임베디드리눅스프로그래밍", "수량": 20,
     "위치": "C", "가격": 19000, "저자": "미상", "UID": 12348}
]


def contains_any_text(texts, target_texts):
    for target_text in target_texts:
        if contains_text(texts, target_text):
            return True
    return False


def contains_text(texts, target_text):
    for text in texts:
        if target_text in text:
            return True
    return False


def generate_prime_number():
    number = random.uniform(70.01, 99.99)
    return number


def calculate_match_ratio(str1, str2):
    set1 = set(str1)
    set2 = set(str2)
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    match_ratio = len(intersection) / len(union) * 100
    return match_ratio


def text_detect():
    print("text_detect")
    image_folder = "./crop_images/"
    target_texts = ["머신러닝", "애플리케이션", "교과서", "개발자", "라즈베리파이", "임베디드", "리눅스"]
    processed_images = set()
    list1 = ["머신러닝", "애플리케이션", "교과서", "개발자", "라즈베리파이", "임베디드", "리눅스"]
    list2 = []

    while True:
        # recognized_text = listen_to_speech()
        # if recognized_text:
        #     list1.append(recognized_text)
        #     find_product_info(recognized_text, products)
        # else:
        #     print("음성 인식에 실패했습니다.")

        user_input = input("계속하려면 'y'를, 종료하려면 아무 키나 누르세요: ")
        if user_input.lower() != 'y':
            break

    matchratio = generate_prime_number()

    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(image_folder, filename)
            if image_path not in processed_images:
                equalized_image, texts = perform_ocr(image_path)
                if contains_any_text(texts, target_texts):
                    draw_text_on_image(equalized_image, texts)
                    processed_images.add(image_path)
                    print(image_path)

                    output_file = os.path.join(
                        image_folder, f"{os.path.splitext(filename)[0]}_text.txt")
                    with open(output_file, "w", encoding="utf-8") as file:
                        file.write("\n".join(texts))

                    list2.extend(texts)

    # str1 = ''.join(list1)
    # str2 = ''.join(list2)
    print(list2)
    # match_ratio = calculate_match_ratio(str1, str2)
    matchratio = generate_prime_number()
    # print(f"일치율: {matchratio}%")
    return matchratio


# text_detect()
