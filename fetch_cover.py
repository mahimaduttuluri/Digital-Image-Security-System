import requests
import time
import cv2
import numpy as np

def fetch_cover_image(encrypted_image_path, output_path="cover_image.png"):
    """Fetch a random PNG cover image and resize it to match the encrypted image."""
    
    url = "https://loremflickr.com/512/512/png"

    encrypted_img = cv2.imread(encrypted_image_path)
    if encrypted_img is None:
        print("Error: Encrypted image not found.")
        return None

    h, w, _ = encrypted_img.shape

    for _ in range(3):
        try:
            response = requests.get(url, timeout=10, stream=True)
            if response.status_code == 200:
                cover_img_array = np.asarray(bytearray(response.raw.read()), dtype=np.uint8)
                cover_img = cv2.imdecode(cover_img_array, cv2.IMREAD_COLOR)

                if cover_img is None:
                    print("⚠️ Error decoding image. Retrying...")
                    continue

                resized_cover_img = cv2.resize(cover_img, (w, h))

                cv2.imwrite(output_path, resized_cover_img, [cv2.IMWRITE_PNG_COMPRESSION, 0])
                print(f"Cover image resized and saved as {output_path}")
                return output_path
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error fetching image: {e}. Retrying...")
            time.sleep(5)

    print("Failed to fetch cover image after multiple attempts.")
    return None

encrypted_image_path = "encrypted_image.png"
fetch_cover_image(encrypted_image_path)
