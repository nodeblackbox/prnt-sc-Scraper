# from selenium import webdriver
# from undetected_chromedriver import Chrome, ChromeOptions
# import os
# import random
# import string
# import time
# import requests
# from bs4 import BeautifulSoup
# from PIL import Image
# import requests
# from io import BytesIO

# def random_string(length):
#     return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


# def download_image(image_url, folder, identifier):
#     known_width = 640
#     known_height = 480
#     # Check if the URL is relative and, if so, prepend it with 'https://'
#     if image_url.startswith('//'):
#         image_url = 'https:' + image_url

#     response = requests.get(image_url)
#     if response.status_code == 200:
#         # Use PIL to check the dimensions of the image
#         img = Image.open(BytesIO(response.content))
#         width, height = img.size
        
#         # If the image dimensions match the known size of the placeholder image, skip saving
#         if width == known_width and height == known_height:
#             print(f"Placeholder image detected for {identifier}, skipping download.")
#             return

#         image_path = os.path.join(folder, f'image_{identifier}.png')
#         with open(image_path, 'wb') as file:
#             img.save(file)

# def save_page_content(driver, identifier, output_file, images_folder):
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     image_container = soup.find('div', class_='image-container')
    
#     if image_container:
#         img_tag = image_container.find('img', class_='screenshot-image')
#         if img_tag and 'src' in img_tag.attrs:
#             image_url = img_tag['src']
#             download_image(image_url, images_folder, identifier)
#             with open(output_file, 'a', encoding='utf-8') as file:
#                 file.write(f"--- Content from {identifier} ---\n")
#                 file.write(str(image_container))
#                 file.write("\n\n")

# def main(base_url, iterations, output_file, images_folder):
#     options = ChromeOptions()
#     options.add_argument("--headless")
#     driver = Chrome(options=options)

#     if not os.path.exists(images_folder):
#         os.makedirs(images_folder)

#     for _ in range(iterations):
#         identifier = random_string(6)
#         url = f"{base_url}{identifier}"
#         print(f"Processing identifier: {identifier}")
#         driver.get(url)
#         # time.sleep(2)
#         save_page_content(driver, identifier, output_file, images_folder)

#     driver.quit()

# # Example usage
# base_url = 'https://prnt.sc/'  # Replace with your base URL
# iterations = 10
# output_file = 'output.txt'
# images_folder = 'images'

# main(base_url, iterations, output_file, images_folder)

























# import os
# import random
# import string
# import requests
# from bs4 import BeautifulSoup
# from PIL import Image
# from io import BytesIO
# from undetected_chromedriver import Chrome, ChromeOptions
# from concurrent.futures import ThreadPoolExecutor
# from queue import Queue

# def random_string(length):
#     return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# def download_image(image_url, folder, identifier):
#     if image_url.startswith('//'):
#         image_url = 'https:' + image_url

#     response = requests.get(image_url)
#     if response.status_code == 200:
#         with Image.open(BytesIO(response.content)) as img:
#             width, height = img.size
#             if width != 640 or height != 480:  # Check for placeholder image size
#                 image_path = os.path.join(folder, f'{identifier}.png')
#                 img.save(image_path)

# def save_page_content(driver, images_folder, identifier):
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     image_container = soup.find('div', class_='image-container img.screenshot-image')
#     if image_container:
#         image_url = image_container.get('src')
#         download_image(image_url, images_folder, identifier)

# def init_driver():
#     chrome_options = ChromeOptions()
#     chrome_options.add_argument("--headless")
#     driver = Chrome(options=chrome_options)
#     return driver

# def scrape_site(base_url, identifier, images_folder, driver):
#     url = f"{base_url}{identifier}"
#     driver.get(url)
#     save_page_content(driver, images_folder, identifier)

# def worker(base_url, images_folder, task_queue, driver):
#     while True:
#         identifier = task_queue.get()
#         if identifier is None:
#             # Sentinel encountered, exit thread
#             break
#         scrape_site(base_url, identifier, images_folder, driver)
#         task_queue.task_done()

# def main(base_url, iterations, images_folder, num_threads=5):
#     if not os.path.exists(images_folder):
#         os.makedirs(images_folder)

#     drivers = [init_driver() for _ in range(num_threads)]
#     task_queue = Queue()

#     # Start worker threads
#     with ThreadPoolExecutor(max_workers=num_threads) as executor:
#         for driver in drivers:
#             executor.submit(worker, base_url, images_folder, task_queue, driver)
        
#         # Queue tasks
#         for _ in range(iterations):
#             identifier = random_string(6)
#             task_queue.put(identifier)

#         # Add sentinels to stop workers
#         for _ in range(num_threads):
#             task_queue.put(None)

#     # Cleanup drivers
#     for driver in drivers:
#         driver.quit()

# # Example usage
# base_url = 'https://prnt.sc/'
# iterations = 10  # Increase or decrease based on your requirement
# images_folder = 'images'

# main(base_url, iterations, images_folder)













# import requests
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from undetected_chromedriver import Chrome, ChromeOptions
# from bs4 import BeautifulSoup
# import random
# import string
# import time
# from PIL import Image
# # import pytesseract
# import os
# import tempfile
# import pyautogui

# def generate_random_string(length):
#     characters = string.ascii_letters + string.digits
#     return ''.join(random.choice(characters) for _ in range(length)).lower()

# def scrape_element(url, element_selector, save_path, driver):
#     options = ChromeOptions()
#     options.add_argument('--headless')  # Run Chrome in headless mode (without a graphical user interface)
#     driver.get(url)
#     try:
#         # Wait for the target element to be present on the page
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element_selector)))

#         # Find the desired element using the provided ID
#         target_element = driver.find_element(By.ID, element_selector)

#         # Check if the element is found
#         if target_element and target_element.get_attribute('src'):
#             image_url = target_element.get_attribute('src')

#             # Download the image using requests
#             response = requests.get(image_url)

#             if response.status_code == 200:
#                 with open(save_path, 'wb') as f:
#                     f.write(response.content)
#                 print(f"Downloaded image from {image_url} to {save_path}")
#             else:
#                 print(f"Failed to download image. Status code: {response.status_code}")
#         else:
#             print(f"Element with ID '{element_selector}' not found!")
#     except Exception as e:
#         print(f"Error: {e}")



# def display_image(image_path):
#     if os.path.exists(image_path):
#         img = Image.open(image_path)
        
#         # Convert the image to 'RGB' mode
#         img = img.convert('RGB')
        
#         img.show()
#         time.sleep(1)  # Display the image for 2 seconds

#         # Save the image to a temporary file to close the display window
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img:
#             temp_img_path = temp_img.name
#             img.save(temp_img_path)

#         # Close the original image
#         img.close()

#         # Close the image window using pyautogui
#         pyautogui.hotkey("alt", "f4")

#         # Remove the temporary file
#         os.remove(temp_img_path)
#     else:
#         print(f"Image file not found: {image_path}")

# base_url = 'https://prnt.sc/'
# element_selector = 'screenshot-image'
# random_string_length = 6

# options = ChromeOptions()
# options.add_argument('--headless')  # Run Chrome in headless mode (without a graphical user interface)
# driver = Chrome(options=options)

# while True:
#     random_string = generate_random_string(random_string_length)
#     updated_url = base_url + random_string
#     save_path = f'image_{random_string}.png'
#     scrape_element(updated_url, element_selector, save_path, driver)
#     display_image(save_path)
#     # Optionally, you can uncomment the line below to close the Chrome driver after displaying each image
#     # driver.quit()


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