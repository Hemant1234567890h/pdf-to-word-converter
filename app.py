from flask import Flask, render_template, request, send_file
import os
from pdf2docx import Converter
from werkzeug.utils import secure_filename

# Define the template folder location explicitly
app = Flask(__name__, template_folder='.')  # Set root folder as template folder

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')  # Flask will now search in the root folder

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf_file' not in request.files:
        return "No file uploaded", 400

    pdf_file = request.files['pdf_file']
    filename = secure_filename(pdf_file.filename)
    pdf_path = os.path.join(UPLOAD_FOLDER, filename)
    pdf_file.save(pdf_path)

    docx_filename = filename.rsplit('.', 1)[0] + '.docx'
    docx_path = os.path.join(UPLOAD_FOLDER, docx_filename)

    cv = Converter(pdf_path)
    cv.convert(docx_path, start=0, end=None)
    cv.close()

    return send_file(docx_path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
