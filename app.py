# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from create_database import generate_data_store
from query_data import query_database
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
UPLOAD_FOLDER = 'data'
ALLOWED_EXTENSIONS = {'pdf'}
CHROMA_PATH = 'chroma'
SECRET_KEY = os.urandom(24)

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB upload limit

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        # Check if the post request has the files part
        if 'files[]' not in request.files:
            flash('No file part in the request.')
            return redirect(request.url)
        
        files = request.files.getlist('files[]')
        if not files or files[0].filename == '':
            flash('No files selected for uploading.')
            return redirect(request.url)
        
        # Save files
        new_files_saved = False
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if not os.path.exists(file_path):  # Avoid duplicates
                    file.save(file_path)
                    new_files_saved = True
                    logger.info(f"Saved new file: {filename}")
                else:
                    flash(f'File "{filename}" already exists and was skipped.')
            else:
                flash(f'File "{file.filename}" is not allowed. Only PDF files are accepted.')
                return redirect(request.url)
        
        if new_files_saved:
            # Append new documents to the Chroma database
            try:
                generate_data_store()
                flash('Files successfully uploaded and processed.')
            except Exception as e:
                logger.error(f'Error processing files: {e}')
                flash(f'An error occurred while processing files: {e}')
                return redirect(request.url)
        else:
            flash('No new files were uploaded.')
        
        return redirect(url_for('upload_files'))
    
    return render_template('upload.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
    response = None
    sources = []
    if request.method == 'POST':
        question = request.form.get('question')
        if not question or question.strip() == '':
            flash('Please enter a valid question.')
            return redirect(request.url)
        
        try:
            response, sources = query_database(question)
            if not response:
                flash('Unable to find matching results. Please try a different question.')
        except Exception as e:
            logger.error(f'Error generating response: {e}')
            flash(f'An error occurred while generating the response: {e}')
    
    return render_template('query.html', response=response, sources=sources)

@app.errorhandler(413)
def request_entity_too_large(error):
    flash('File is too large. Maximum upload size is 16MB.')
    return redirect(request.url), 413

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Run the app
if __name__ == '__main__':
    # Initialize Chroma only if it doesn't exist and there are documents
    if not os.path.exists(CHROMA_PATH):
        logger.info("Initializing Chroma database...")
        try:
            generate_data_store()
            logger.info("Chroma database initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Chroma database: {e}")
            # Optionally, you might want to exit the application or handle it accordingly
    app.run(debug=True)
