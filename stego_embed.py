import cv2
import numpy as np
from fetch_cover import fetch_cover_image

def embed_image(cover_image_path, secret_image_path, output_path):
    """Embed a full RGB encrypted image into the cover image using LSB steganography."""
    cover_img = cv2.imread(cover_image_path)
    cover_img = cv2.cvtColor(cover_img, cv2.COLOR_BGR2RGB)

    secret_img = cv2.imread(secret_image_path)
    secret_img = cv2.cvtColor(secret_img, cv2.COLOR_BGR2RGB)

    h, w, c = cover_img.shape
    assert secret_img.shape == (h, w, c), "Error: Cover and encrypted images must have the same dimensions!"

    stego_img = np.copy(cover_img)
    for i in range(3):
        stego_img[:, :, i] = (cover_img[:, :, i] & 0b11111100) | ((secret_img[:, :, i] >> 6) & 0b11)


    # Save stego image
    print(f"✅ Verifying: Stego Image LSB Before Saving (Pixel[0,0]): {bin(stego_img[0,0,0] & 0b11)}")
    stego_img = cv2.cvtColor(stego_img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, stego_img, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    return output_path

if __name__ == "__main__":
    cover_image_path = fetch_cover_image("encrypted_image.png")

    secret_image_path = "encrypted_image.png"
    output_stego = "stego_image.png"

    if cover_image_path:
        embed_image(cover_image_path, secret_image_path, output_stego)
        print(f"✅ Stego image saved as {output_stego}")
    else:
        print("Failed to fetch cover image.")

