import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import logistic_map_sequence, sha256_key_from_image

def encrypt_image(image_path):
    """Encrypt a color image using chaotic Logistic Map with SHA-256 key."""
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, c = img.shape

    # 🔑 Generate the key from the original image
    key = sha256_key_from_image(img)
    print(f"🔑 Generated Key from SHA-256: {key}")

    # ✅ Save the key to a file
    with open("encryption_key.txt", "w") as f:
        f.write(str(key))

    encrypted_channels = []
    for i in range(c):
        channel = img[:, :, i].flatten()
        chaotic_seq = logistic_map_sequence(h * w, key + i * 0.01)
        encrypted_channel = np.bitwise_xor(channel, chaotic_seq)
        encrypted_channels.append(encrypted_channel.reshape((h, w)))

    encrypted_img = np.stack(encrypted_channels, axis=2)
    cv2.imwrite("encrypted_image.png", cv2.cvtColor(encrypted_img, cv2.COLOR_RGB2BGR))
    
    return encrypted_img

image_path = "/Users/macbook/Downloads/sample.png"  
encrypted_img = encrypt_image(image_path)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(cv2.imread(image_path)[..., ::-1])  
plt.title("Original Image")

plt.subplot(1, 2, 2)
plt.imshow(encrypted_img)
plt.title("Encrypted Image")

plt.show()