from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import subprocess

# Initialize the Flask application
app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}

AUDIO_UPLOAD_FOLDER = '.DeepVoiceDetection/data/real/'

# Configure the upload folder and allowed file types
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if file has allowed extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define the main route
@app.route("/")
def hello():
    return "This is the main page"

# Define the user route which supports GET and POST methods
@app.route("/user", methods=['GET', 'POST'])
def post():
    if request.method == 'GET':
        return "HI"

@app.route("/audio", methods=['POST'])
def audio():
    # Check if the request has a file part
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']

    # If no file is selected, return an error
    if file.filename == '':
        return 'No selected file'

    # Save the file
    filename = secure_filename(file.filename)
    filepath = os.path.join(AUDIO_UPLOAD_FOLDER, filename)
    file.save(filepath)
    return filepath

    # Pass the file path to train.py script and capture the output
    result = subprocess.run(['python', 'train.py'], stdout=subprocess.PIPE)
    return result.stdout.decode()

# Define the gpt route which supports file upload and processing
@app.route("/gpt", methods=['GET', 'POST'])
def gpt():
    # If the request method is POST, process the file
    if request.method == 'POST':
        # Check if the request has a file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']

        # If no file is selected, return an error
        if file.filename == '':
            return 'No selected file'

        # If file is selected and is of allowed type, save it and pass it to gpt_api.py script
        if file and allowed_file(file.filename):
            # Save the file securely to avoid security issues
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Pass the file path to gpt_api.py script and capture the output
            result = subprocess.run(['python', 'gpt_api.py', filepath], stdout=subprocess.PIPE)
            return result.stdout.decode()
        else:
            return 'Invalid file type'

    # If the request method is GET, display the file upload form
    return '''
    <!doctype html>
    <title>Upload a text file</title>
    <h1>Upload a text file</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# Main entry point for the script
if __name__ == "__main__":
    # Create upload directory if it does not exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    # Run the Flask application
    app.run(host='0.0.0.0')
