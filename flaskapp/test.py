import cv2
import numpy as np

def process_image(image_path):
    
    image = cv2.imread(image_path)
    if image is None:
        print("Error loading image")
        return

    green_channel = image[:, :, 1]

    mean_green = np.mean(green_channel)
    binary_image = np.zeros_like(green_channel, dtype=np.uint8)

    black_pixel_count = 0
    total_pixels = green_channel.size

    for i in range(green_channel.shape[0]):
        for j in range(green_channel.shape[1]):
            gray = green_channel[i, j]

            if gray < mean_green / 1.5:
                binary_image[i, j] = 0
                black_pixel_count += 1
            else:
                binary_image[i, j] = 255

    green_cover_percentage = (black_pixel_count / total_pixels) * 100
    idle_land_percentage = 100 - green_cover_percentage

    print(f"Green Cover Percentage: {green_cover_percentage:.2f}%")
    print(f"Idle Land Percentage: {idle_land_percentage:.2f}%")

    processed_image_path = 'processed_image.png'
    cv2.imwrite(processed_image_path, binary_image)
    print(f"Processed image saved as {processed_image_path}")

process_image(r'D:\Projects\EDI TY SEM 2\TYEDI-2\flaskapp\optimaltest.png')
