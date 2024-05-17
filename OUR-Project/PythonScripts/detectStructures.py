import cv2
import numpy as np

# Function to load and preprocess the image
def load_and_preprocess_image(image_path):
    try:
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError("Image file not found or couldn't be read.")
        
        # Preprocess the image (convert to grayscale, apply Gaussian blur, etc.)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        return image, blurred
    except Exception as e:
        print("Error loading and preprocessing the image:", str(e))
        return None, None

# Function to detect contours and draw them on the image
def detect_and_draw_contours(image, edges):
    try:
        # Edge detection using Canny
        edges = cv2.Canny(edges, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw contours on the original image
        contour_image = np.zeros_like(image)
        cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 6)
        
        return contour_image
    except Exception as e:
        print("Error detecting and drawing contours:", str(e))
        return None

# Main function
def main():
    # Path to the image file
    image_path = r'D:\Projects\EDI TY SEM 2\TYEDI-2\OUR-Project\PythonScripts\forest2.webp'

    # Load and preprocess the image
    original_image, blurred_image = load_and_preprocess_image(image_path)
    if original_image is None or blurred_image is None:
        print("Unable to load and preprocess the image. Please check the file path.")
        return

    # Detect contours and draw them on the image
    contour_image = detect_and_draw_contours(original_image, blurred_image)
    if contour_image is None:
        print("Unable to detect contours.")
        return

    # Display the result
    cv2.imshow('Original Image', original_image)
    cv2.imshow('Contours', contour_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Call the main function
if __name__ == "__main__":
    main()
