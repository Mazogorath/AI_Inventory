import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import requests
import time

searchKey = input('검색 키워드 입력:')

# Create a directory with the search key name if it does not exist
folder_name = searchKey.replace(" ", "_")  # Replace spaces with underscores for folder name
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

driver = webdriver.Chrome()
driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
elem = driver.find_element(By.NAME, "q")

elem.send_keys(searchKey)
elem.send_keys(Keys.RETURN)

# Wait for the page to load and then find the image elements
driver.implicitly_wait(10)  # You may need to adjust the wait time based on your network speed
images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
counter = 1
for image in images:
    image.click()
    try:
        # Find the element with the specified class
        img_element = driver.find_element(By.CLASS_NAME, "sFlh5c.pT0Scc.iPVvYb")
        image_url = img_element.get_attribute("src")

        # Download the image if the URL ends with .jpeg or .jpg
        if image_url.endswith(".jpeg") or image_url.endswith(".jpg"):
            image_data = requests.get(image_url).content
            with open(f"{folder_name}/{str(counter).zfill(4)}.jpg", "wb") as f:
                f.write(image_data)
            print(f"Image {str(counter).zfill(4)}.jpg downloaded successfully")
            counter += 1
        else:
            print("Image format not supported")
    except NoSuchElementException:
        print("Image element not found")

driver.quit()