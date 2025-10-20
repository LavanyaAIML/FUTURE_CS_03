from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from cryptography.fernet import Fernet
import os

app = Flask(__name__)
app.secret_key = "supersecretflaskkey"  # For session security
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------- AES KEY MANAGEMENT --------
KEY_FILE = "secret.key"

def generate_key():
    """Generate and save AES key (once)."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

def load_key():
    """Load AES key."""
    return open(KEY_FILE, "rb").read()

generate_key()
fernet = Fernet(load_key())

# -------- ROUTES --------

@app.route("/")
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", files=files)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if file.filename == "":
            flash("No file selected")
            return redirect(request.url)

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file_data = file.read()
        encrypted_data = fernet.encrypt(file_data)

        with open(filepath, "wb") as f:
            f.write(encrypted_data)

        flash("File uploaded and encrypted successfully!")
        return redirect(url_for("index"))
    return render_template("upload.html")

@app.route("/download/<filename>")
def download(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, "rb") as f:
        encrypted_data = f.read()
        decrypted_data = fernet.decrypt(encrypted_data)

    decrypted_path = os.path.join("uploads", "decrypted_" + filename)
    with open(decrypted_path, "wb") as f:
        f.write(decrypted_data)

    return send_file(decrypted_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
