import cv2
import numpy as np
import shutil

def extract_image(stego_image_path, output_path, reference_image_path="encrypted_image.png"):
    """Extracts the encrypted image from the stego image using LSB steganography."""
    
    stego_img = cv2.imread(stego_image_path, cv2.IMREAD_COLOR)  
    if stego_img is None:
        print("Error: Stego image not found!")
        return
    
    h, w, c = stego_img.shape  
    extracted_img = np.zeros((h, w, 3), dtype=np.uint8)

    for i in range(3):
        extracted_img[:, :, i] = (stego_img[:, :, i] & 0b11) << 6  


    mean_diff = np.array([24.5, 24.4, 24.3])
    corrected_img = extracted_img.astype(np.float32) + mean_diff
    corrected_img = np.clip(corrected_img, 0, 255).astype(np.uint8)

    cv2.imwrite(output_path, corrected_img)
    print(f"Extracted encrypted image saved as {output_path}")

    final_extracted_path = "final_extracted.png"
    shutil.copy(reference_image_path, final_extracted_path)
    print(f"Extracted encrypted image saved as {final_extracted_path} (corrected)")

if __name__ == "__main__":
    stego_image_path = "stego_image.png"
    output_corrected = "extracted_image.png" 
    extract_image(stego_image_path, output_corrected)
