import cv2
import numpy as np


# def findOptimalsite(height , width , image):

#     heightMap = [0 for i in range(width)]
#     widthMap = [0 for i in range(height)]

#     height,width,channel = image.shape

#     minimumGreenCoverage = height*width
#     x,y = 0,0

#     currentGreenCoverage = 0

#     for i in range(height):

#         for j in range(width):

#             if(image[i,j] == 255):

#                 heightMap[j] += 1
#                 widthMap[i] += 1
#                 currentGreenCoverage+=1


def convolution_sum(matrix, km,kn):
    m, n = matrix.shape
    result = 0
    mresult = 0
    cords = (0,0)
    for i in range(m-km+1):
        for j in range(n-kn+1):
            result = np.sum(matrix[i:i+km, j:j+kn])

            if(result > mresult):

                mresult = result
                cords = (j,i)

    return cords


# def min_sum_submatrix(matrix, height, width):
#     rows,cols = matrix.shape

#     min_sum = float('inf')
#     min_submatrix = None

#     cords = (0,0)

#     for x in range(height):
#         for y in range(width):
#             submatrix_sum += matrix[i + x][j + y]

#     for i in range(rows - height + 1):
#         for j in range(cols - width + 1):
#             # Calculate the sum of the current submatrix
#             submatrix_sum = 0
            

#             # Update minimum sum and submatrix if necessary
#             if submatrix_sum < min_sum:
#                 cords = (i,j)
#                 min_sum = submatrix_sum
#                 min_submatrix = [row[j:j + width] for row in matrix[i:i + height]]

#     return cords



def process_image(image_path, h , w):
    
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

    cords = convolution_sum(binary_image, h , w)
    
    endcords = (cords[0]+h,cords[1]+w)
    print(cords,endcords,binary_image.shape,h,w)

    color = (0, 255, 0)
    thickness = 2

    binary_image = cv2.rectangle(binary_image, cords, endcords , color, thickness)


    processed_image_path = 'processed_image.png'
    cv2.imwrite(processed_image_path, binary_image)
    print(f"Processed image saved as {processed_image_path}")

process_image(r"D:\Projects\EDI TY SEM 2\TYEDI-2\flaskapp\optimaltest.png" , 300, 300)