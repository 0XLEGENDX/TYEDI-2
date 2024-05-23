
import cv2
import numpy as np
import glob

# Prepare object points (0,0,0), (1,0,0), (2,0,0), ..., (8,5,0)
objp = np.zeros((6*9, 3), np.float32)
objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

objpoints = []  # 3D points in real world space
imgpointsL = [] # 2D points in image plane for left camera
imgpointsR = [] # 2D points in image plane for right camera

# Lists of calibration images
images_left = glob.glob(r'C:\Users\anura\OneDrive\Desktop\codes\mid.jpg')
images_right = glob.glob(r'C:\Users\anura\OneDrive\Desktop\codes\right.jpg')

# Ensure the number of images in both lists is the same
if len(images_left) != len(images_right):
    raise ValueError("Number of left and right images must be the same")

# Process each image pair
for img_left, img_right in zip(images_left, images_right):
    imgL = cv2.imread(img_left)
    imgR = cv2.imread(img_right)
    grayL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
    grayR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

    retL, cornersL = cv2.findChessboardCorners(grayL, (9, 6), None)
    retR, cornersR = cv2.findChessboardCorners(grayR, (9, 6), None)

    if retL and retR:
        objpoints.append(objp)
        imgpointsL.append(cornersL)
        imgpointsR.append(cornersR)

        cv2.drawChessboardCorners(imgL, (9, 6), cornersL, retL)
        cv2.drawChessboardCorners(imgR, (9, 6), cornersR, retR)
        cv2.imshow('imgL', imgL)
        cv2.imshow('imgR', imgR)
        cv2.waitKey(500)

cv2.destroyAllWindows()

# Ensure we have valid points
if len(objpoints) == 0 or len(imgpointsL) == 0 or len(imgpointsR) == 0:
    raise ValueError("No valid chessboard corners found in images")

# Calibrate the cameras
retL, mtxL, distL, rvecsL, tvecsL = cv2.calibrateCamera(objpoints, imgpointsL, grayL.shape[::-1], None, None)
retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(objpoints, imgpointsR, grayR.shape[::-1], None, None)

# Stereo calibration
flags = 0
flags |= cv2.CALIB_FIX_INTRINSIC
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-5)
ret, mtxL, distL, mtxR, distR, R, T, E, F = cv2.stereoCalibrate(
    objpoints, imgpointsL, imgpointsR, mtxL, distL, mtxR, distR, grayL.shape[::-1], criteria=criteria, flags=flags)

# Stereo rectification
R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(mtxL, distL, mtxR, distR, grayL.shape[::-1], R, T, alpha=0)

# Compute the rectification maps
mapLx, mapLy = cv2.initUndistortRectifyMap(mtxL, distL, R1, P1, grayL.shape[::-1], cv2.CV_32FC1)
mapRx, mapRy = cv2.initUndistortRectifyMap(mtxR, distR, R2, P2, grayL.shape[::-1], cv2.CV_32FC1)

# Load a pair of rectified images
rectifiedL = cv2.remap(cv2.imread('left_img.jpg'), mapLx, mapLy, cv2.INTER_LINEAR)
rectifiedR = cv2.remap(cv2.imread('right_img.jpg'), mapRx, mapRy, cv2.INTER_LINEAR)

# Compute disparity map
stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(cv2.cvtColor(rectifiedL, cv2.COLOR_BGR2GRAY), cv2.cvtColor(rectifiedR, cv2.COLOR_BGR2GRAY))

# Normalize the disparity map for visualization
disparity_normalized = cv2.normalize(disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

cv2.imshow('Disparity', disparity_normalized)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Reproject to 3D
depth_map = cv2.reprojectImageTo3D(disparity, Q)

# Mask out points with no disparity
mask = disparity > disparity.min()
output_points = depth_map[mask]

# Convert the points to a readable format
output_points = np.array(output_points, dtype=np.float32)

print("3D Points:")
print(output_points)
