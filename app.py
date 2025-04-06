from flask import Flask, render_template, request, send_file, redirect, url_for, Response, session, flash, jsonify
import os
import cv2
import numpy as np
import sqlite3
from encrypt import encrypt_image
from decrypt import decrypt_image
from stego_embed import embed_image, fetch_latest_cover_image, fetch_latest_encrypted_image, save_stego_to_db
from stego_extract import fetch_latest_stego_image, fetch_original_encrypted_image, extract_image, save_extracted_to_db
from fetch_cover import fetch_cover_image
from database import insert_image, fetch_image, insert_user, validate_login
from functools import wraps

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management

# 📁 Ensure 'uploads' directory exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def login_required(f):
    """Decorator to check if the user is logged in before accessing a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("You must be logged in to access this page.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# 🏠 **Home route**
@app.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("signup"))

    # Ensure all buttons are visible initially
    if "show_encrypted" not in session:
        session["show_encrypted"] = False
    if "show_stego" not in session:
        session["show_stego"] = False
    if "show_decrypted" not in session:
        session["show_decrypted"] = False

    return render_template(
        "index.html",
        show_encrypted=session["show_encrypted"],
        show_stego=session["show_stego"],
        show_decrypted=session["show_decrypted"],
    )


# 🔐 **User Signup**
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        insert_user(username, password)  # Register user in the database
        flash("Signup successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


# 🔑 **User Login**
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if validate_login(username, password):
            session["username"] = username  # Store username in session
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")


# 🚪 **User Logout**
@app.route("/logout")
def logout():
    session.pop("username", None)  # Remove user from session
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


# 🔐 **Encryption & Embedding**
@app.route("/encrypt", methods=["POST"])
@login_required
def encrypt():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    image_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(image_path)

    encrypted_img = encrypt_image(image_path)
    fetch_cover_image(image_path)  # ✅ Fetch & store cover image

    image_id, cover_img = fetch_latest_cover_image()
    latest_encrypted_img = fetch_latest_encrypted_image()

    if cover_img is not None and latest_encrypted_img is not None:
        stego_img = embed_image(cover_img, latest_encrypted_img)
        save_stego_to_db(image_id, stego_img)
    else:
        return "Error: Missing cover or encrypted image", 400
    session["show_encrypted"] = True
    session["show_stego"] = True
    session["show_decrypted"] = False
    return redirect(url_for("index"))


# 🔓 **Extract & Decrypt**
@app.route("/extract-decrypt", methods=["POST"])
@login_required
def extract_decrypt():
    image_id, stego_img = fetch_latest_stego_image()
    if stego_img is None:
        return "No stego image found in the database.", 400

    extracted_img = extract_image(stego_img)
    original_encrypted_img = fetch_original_encrypted_image()
    
    if original_encrypted_img is None:
        return "No original encrypted image found in the database.", 400

    save_extracted_to_db(image_id, extracted_img, original_encrypted_img)
    decrypt_image(image_id)
    session["show_encrypted"] = False
    session["show_stego"] = False
    session["show_decrypted"] = True
    return redirect(url_for("index"))


# ⬇️ **Download Images**
@app.route("/download/<filename>")
@login_required
def download(filename):
    """Fetch the requested image from the database and serve it dynamically."""
    conn = sqlite3.connect("encryption.db")
    cursor = conn.cursor()

    column_map = {
        "encrypted_image.png": "encrypted_img",
        "stego_image.png": "stego_img",
        "extracted_encrypted.png": "extracted_encrypted_img",
        "decrypted_image.png": "decrypted_img",
    }

    if filename not in column_map:
        return "File not found", 404

    column_name = column_map[filename]
    cursor.execute(f"SELECT {column_name} FROM images ORDER BY timestamp DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row and row[0]:
        return Response(row[0], mimetype="image/png", headers={"Content-Disposition": f"attachment; filename={filename}"})

    return "File not found in database.", 404


if __name__ == "__main__":
    app.run(debug=True)
