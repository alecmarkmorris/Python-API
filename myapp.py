from flask import Flask, request, jsonify, send_file
from pdf2docx import Converter
import os
import uuid

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_pdf_to_docx():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    pdf_file_path = f'/tmp/{uuid.uuid4()}.pdf'
    docx_file_path = pdf_file_path.replace('.pdf', '.docx')
    
    file.save(pdf_file_path)

    try:
        converter = Converter(pdf_file_path)
        converter.convert(docx_file_path, start=0, end=None)
        converter.close()
        return send_file(docx_file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(pdf_file_path):
            os.remove(pdf_file_path)
        if os.path.exists(docx_file_path):
            os.remove(docx_file_path)

if __name__ == '__main__':
    app.run(debug=True)



