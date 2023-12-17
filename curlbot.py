from selenium import webdriver
from undetected_chromedriver import Chrome, ChromeOptions
import os
import random
import string
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def random_string(length):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def download_image(image_url, folder, identifier):
    if image_url.startswith('//'):
        image_url = 'https:' + image_url

    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with Image.open(BytesIO(response.content)) as img:
                width, height = img.size
                if width != 640 or height != 480:  # Check for placeholder image size
                    image_path = os.path.join(folder, f'{identifier}.png')
                    img.save(image_path)
    except Exception as e:
        print(f"Error downloading image {identifier}: {e}")

def save_page_content(driver, images_folder, identifier):
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        img_tag = soup.find('img', class_='screenshot-image')
        if img_tag and 'src' in img_tag.attrs:
            image_url = img_tag['src']
            print(f"Downloading image for identifier {identifier}: {image_url}")
            download_image(image_url, images_folder, identifier)
        else:
            print(f"No image found for identifier {identifier}")
    except Exception as e:
        print(f"Error processing {identifier}: {e}")


def main(base_url, iterations, images_folder):
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = None
    try:
        driver = Chrome(options=options)
        for i in range(iterations):
            identifier = random_string(6)
            url = f"{base_url}{identifier}"
            print(f"Processing URL: {url}")
            try:
                driver.get(url)
                save_page_content(driver, images_folder, identifier)
            except Exception as e:
                print(f"Error processing URL {url}: {e}")
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
    finally:
        if driver:
            driver.quit()

# Example usage
base_url = 'https://prnt.sc/'
iterations = 100
images_folder = 'images'

main(base_url, iterations, images_folder)