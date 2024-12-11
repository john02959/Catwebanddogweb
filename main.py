from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

# Define upload folders for DogWeb and CatWeb
DOGWEB_FOLDER = "dogweb_storage"
CATWEB_FOLDER = "catweb_storage"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi'}

# Ensure storage directories exist
os.makedirs(DOGWEB_FOLDER, exist_ok=True)
os.makedirs(CATWEB_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/dogweb/upload", methods=["POST"])
def dogweb_upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type or no file selected"}), 400
    filepath = os.path.join(DOGWEB_FOLDER, file.filename)
    file.save(filepath)
    return jsonify({"message": "File uploaded successfully", "dogweb_url": f"dog://{file.filename}"}), 200

@app.route("/catweb/upload", methods=["POST"])
def catweb_upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type or no file selected"}), 400
    filepath = os.path.join(CATWEB_FOLDER, file.filename)
    file.save(filepath)
    return jsonify({"message": "File uploaded successfully", "catweb_url": f"cat://{file.filename}"}), 200

@app.route("/dogweb/<filename>", methods=["GET"])
def dogweb_view(filename):
    filepath = os.path.join(DOGWEB_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    return send_file(filepath)

@app.route("/catweb/<filename>", methods=["GET"])
def catweb_view(filename):
    filepath = os.path.join(CATWEB_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    return send_file(filepath)

@app.route("/dogweb", methods=["GET"])
def dogweb_list():
    files = os.listdir(DOGWEB_FOLDER)
    return jsonify({"dogweb_files": files}), 200

@app.route("/catweb", methods=["GET"])
def catweb_list():
    files = os.listdir(CATWEB_FOLDER)
    return jsonify({"catweb_files": files}), 200

if __name__ == "__main__":
    app.run(debug=True, port=8080)
