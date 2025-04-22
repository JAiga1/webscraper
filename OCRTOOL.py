from flask import Flask, request, jsonify
import cv2
import pytesseract
import numpy as np

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['image']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # Your existing preprocessing and OCR code
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY, 11, 2)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    text = pytesseract.image_to_string(gray, config='--oem 3 --psm 6')
    
    return jsonify({"extracted_text": text})

if __name__ == '__main__':
    app.run(debug=True)
