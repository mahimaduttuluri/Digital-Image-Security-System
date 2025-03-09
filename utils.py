import numpy as np
import hashlib

def sha256_key_from_image(image):
    """Generate a key from the SHA-256 hash of the image pixels."""
    # Flatten image to a 1D array and convert to bytes
    image_bytes = image.flatten().tobytes()
    
    # Compute SHA-256 hash
    hash_digest = hashlib.sha256(image_bytes).hexdigest()
    
    # Convert the first 8 characters of the hash to a floating-point seed (0 to 1)
    key = int(hash_digest[:8], 16) / (16**8)
    return key

def logistic_map_sequence(size, key):
    """Generate a chaotic sequence using the Logistic Map with a dynamic key."""
    x = key  # Key derived from SHA-256
    r = 3.99  # Control parameter for chaos

    sequence = np.zeros(size, dtype=np.float64)
    for i in range(size):
        x = r * x * (1 - x)
        sequence[i] = x
    
    return (sequence * 255).astype(np.uint8)  # Normalize to 0-255