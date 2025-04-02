import cv2
import pytesseract
import numpy as np

image_path = "sample_image.png"
image = cv2.imread(image_path)

# Check if image loaded
if image is None:
    print("Error: Could not load image.")
    exit()

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding to handle varying lighting
gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                            cv2.THRESH_BINARY, 11, 2)

# Optional: Remove noise with a blur
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# OCR with some config tweaks
custom_config = r'--oem 3 --psm 6'  # OEM 3 = default, PSM 6 = assume a single uniform block of text
text = pytesseract.image_to_string(gray, config=custom_config)

print("Extracted Text:\n", text)
