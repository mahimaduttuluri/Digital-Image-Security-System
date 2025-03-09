import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import logistic_map_sequence

def decrypt_image(encrypted_image_path):
    """Decrypt a color image using the saved key from encryption."""
    encrypted_img = cv2.imread(encrypted_image_path)
    encrypted_img = cv2.cvtColor(encrypted_img, cv2.COLOR_BGR2RGB)
    h, w, c = encrypted_img.shape  

    # 🔑 Load the saved key from encryption
    with open("encryption_key.txt", "r") as f:
        key = float(f.read().strip())
    print(f"🔑 Loaded Key for Decryption: {key}")

    decrypted_channels = []
    for i in range(c):
        channel = encrypted_img[:, :, i].flatten()
        chaotic_seq = logistic_map_sequence(h * w, key + i * 0.01)
        decrypted_channel = np.bitwise_xor(channel, chaotic_seq)
        decrypted_channels.append(decrypted_channel.reshape((h, w)))

    decrypted_img = np.stack(decrypted_channels, axis=2)
    cv2.imwrite("decrypted_image.png", cv2.cvtColor(decrypted_img, cv2.COLOR_RGB2BGR))

    return decrypted_img

encrypted_image_path = "encrypted_image.png"
decrypted_img = decrypt_image(encrypted_image_path)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(cv2.imread(encrypted_image_path)[..., ::-1])  
plt.title("Encrypted Image")

plt.subplot(1, 2, 2)
plt.imshow(decrypted_img)
plt.title("Decrypted Image")

plt.show()