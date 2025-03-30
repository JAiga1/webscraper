import cv2
import pytesseract

# Load image
image_path = "sample_image.png"  # Change to your image path
image = cv2.imread(image_path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply OCR
text = pytesseract.image_to_string(gray)

# Print extracted text
print("Extracted Text:\n", text)
