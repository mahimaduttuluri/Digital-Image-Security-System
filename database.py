import sqlite3

def initialize_db():
    """Create SQLite database and images table if it doesn't exist."""
    conn = sqlite3.connect("encryption.db")
    cursor = conn.cursor()

    # Create table to store images
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_name TEXT,
            original_img BLOB,  -- Optional: Store original image if needed
            encrypted_img BLOB,
            extracted_encrypted_img BLOB,  -- Store extracted encrypted image
            cover_img BLOB,
            stego_img BLOB,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def insert_image(original_name, original_img, encrypted_img, extracted_encrypted_img, cover_img, stego_img):
    """Insert an image into the database."""
    conn = sqlite3.connect("encryption.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO images (original_name, original_img, encrypted_img, extracted_encrypted_img, cover_img, stego_img)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (original_name, original_img, encrypted_img, extracted_encrypted_img, cover_img, stego_img))

    conn.commit()
    conn.close()

def fetch_image(image_id):
    """Fetch an image from the database by ID."""
    conn = sqlite3.connect("encryption.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM images WHERE id = ?", (image_id,))
    image_data = cursor.fetchone()

    conn.close()
    return image_data

def delete_image(image_id):
    """Delete an image from the database by ID."""
    conn = sqlite3.connect("encryption.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM images WHERE id = ?", (image_id,))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
    print("✅ Database initialized successfully.")
