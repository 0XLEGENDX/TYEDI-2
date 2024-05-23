import cv2
import numpy as np
import pandas as pd
from highres_stereo import HighResStereo
from highres_stereo.utils_highres import Config, CameraConfig, draw_disparity, draw_depth, QualityLevel

def downgrade_image(img, method="average", scale=0.5):

    if method == "average":
        # Downsample using averaging (box filter)
        kernel_size = 3  # Adjust kernel size for desired blur level
        lq_img = cv2.blur(img, (kernel_size, kernel_size))

    elif method == "bicubic":
        # Downsample using bicubic interpolation (better quality)
        height, width = img.shape[:2]
        new_height = int(height * scale)
        new_width = int(width * scale)
        lq_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

    elif method == "resize":
        # Simple resize (may introduce artifacts)
        lq_img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    else:
        raise ValueError(f"Invalid downsampling method: {method}")

    return lq_img

def heightEstimate(distanceFromCameraToTerrain=5):
    
    config = Config(clean=-1, qualityLevel = QualityLevel.High, max_disp=128, img_res_scale=1)
    use_gpu = True
    model_path = r"D:\Projects\EDI TY SEM 2\TYEDI-2\flaskapp\modules\models\final-768px.tar"

    left_img = cv2.imread(r"D:\Projects\EDI TY SEM 2\TYEDI-2\flaskapp\static\uploads\imageUploadedLeft.jpg")
    right_img = cv2.imread(r"D:\Projects\EDI TY SEM 2\TYEDI-2\flaskapp\static\uploads\imageUploadedRight.jpg")

    downgraded_left_img = downgrade_image(left_img, method="bicubic", scale=0.5)
    downgraded_right_img = downgrade_image(right_img, method="bicubic", scale=0.5)

    # Initialize model
    highres_stereo_depth = HighResStereo(model_path, config, use_gpu=use_gpu)

    # Estimate the depth
    disparity_map = highres_stereo_depth(downgraded_left_img, downgraded_right_img)

    color_disparity = draw_disparity(disparity_map)
 
    cv2.imwrite("downgraded_left_img_out.jpg", downgraded_left_img)
    cv2.imwrite("downgraded_right_img_out.jpg", downgraded_right_img)


    cv2.imwrite("out.jpg", color_disparity)
    img = cv2.imread('out.jpg')
    
    height , width , channels = img.shape

    maxheight = 0
    minheight = 255

    for i in range(height):
        for j in range(width):

            b,g,r = img[i,j]
            if(r >= b and r >= b):

                if(r>maxheight):
                    maxheight = r
                

            else:

                minheight = min(b,g)

    return distanceFromCameraToTerrain* ((255 - (maxheight - minheight) )/255)

# heightEstimate()