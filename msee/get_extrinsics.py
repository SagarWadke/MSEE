import cv2
import numpy as np
import pandas as pd
import glob
import os
import re
from msee.utils import show_image
from msee.extended_analysis import analysis

# Load the camera matrix from a YAML file
def load_camera_matrix(yaml_file):
    fs = cv2.FileStorage(yaml_file, cv2.FILE_STORAGE_READ)
    # Read camera matrix
    camera_matrix = fs.getNode('camera_matrix').mat()
    fs.release()
    return camera_matrix

# Load the distortion coefficients from a YAML file
def load_distortion_coeffs(yaml_file):
    fs = cv2.FileStorage(yaml_file, cv2.FILE_STORAGE_READ)
    # Read distortion coefficients
    dist_coeffs = fs.getNode('distortion_coefficients').mat()
    fs.release()
    return dist_coeffs

def extract_number(filename):
    match = re.search(r'_(\d+)\.', filename)  # Search for the pattern _<digits>.
    if match:
        return int(match.group(1))  # Convert the captured digits to an integer
    return None


df = pd.DataFrame({
    'Img_name':[],
    'X_theta': [],
    'Y_theta': [],
    'Z_theta': [],
    'obj_x': [],
    'obj_y': [],
    'obj_z': [],
    'R_cam_X_theta':[],
    'R_cam_Y_theta':[],
    'R_cam_Z_theta':[],
    'cam_x': [],
    'cam_y': [],
    'cam_z': []
})

print('\n Please enter the following reqired parameters:\n')

input_str = input("\n Enter chessboard size (row,col): ")  # e.g., "9,14"
x_str, y_str = input_str.strip().split(',')
chessboardSize = (int(x_str), int(y_str)) 

input_str = input("\n Enter the size of chessboard square in mm: ") 
size_of_chessboard_squares_mm = int(input_str)  # e.g., 18.0

image_format_input = input("\n Enter the image format (e.g., 'png' or 'jpg'): ")  # e.g., " png "
image_format = f"*.{image_format_input.strip()}"  # Converts " png " to "*.png", "*.png"

print(f"\n The image format is: {image_format}")
print(f"\n The chessboard size is: {chessboardSize}")
print(f"\n The size of chessboard squares is: {size_of_chessboard_squares_mm} mm")

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

objp = objp * size_of_chessboard_squares_mm

images = glob.glob(image_format)

for image in images:
    Img_name = os.path.basename(image)
    
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)
    if not ret:
        print(f"Chessboard corners not found in {Img_name}. Skipping this image.")
        continue  # Skip to the next image

    corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
    imgp = corners2

    # Draw and display the corners
    cv2.drawChessboardCorners(img, chessboardSize, corners2, ret)
    #cv.imshow('png', img)
    show_image(img)

    camera_matrix = load_camera_matrix('camera_matrix.yml')
    distortion_coefficients = load_distortion_coeffs('distortion_coeffs.yml')

    success, rvec_cal, tvec_cal = cv2.solvePnP(objp, imgp, camera_matrix, distCoeffs=distortion_coefficients)

    rvec = rvec_cal
    tvec = tvec_cal

    # Convert rvec to rotation matrix
    R, _ = cv2.Rodrigues(rvec)

    sy = np.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
    singular = sy < 1e-6
    if not singular:
        x = np.arctan2(R[2, 1], R[2, 2])
        y = np.arctan2(-R[2, 0], sy)
        z = np.arctan2(R[1, 0], R[0, 0])
    else:
        x = np.arctan2(-R[1, 2], R[1, 1])
        y = np.arctan2(-R[2, 0], sy)
        z = 0

    X_theta = x
    Y_theta = y
    Z_theta = z

    obj_x = tvec[0]
    obj_y = tvec[1]
    obj_z = tvec[2]

    R_cam = R.T

    sy = np.sqrt(R_cam[0, 0] * R_cam[0, 0] + R_cam[1, 0] * R_cam[1, 0])
    singular = sy < 1e-6
    if not singular:
        p = np.arctan2(R[2, 1], R[2, 2])
        q = np.arctan2(-R[2, 0], sy)
        r = np.arctan2(R[1, 0], R[0, 0])
    else:
        p = np.arctan2(-R[1, 2], R[1, 1])
        q = np.arctan2(-R[2, 0], sy)
        r = 0

    R_cam_X_theta = p
    R_cam_Y_theta = q
    R_cam_Z_theta = r

    #camera_position = -np.dot(R.T, tvec)
    camera_position = -R_cam @ tvec
    # Undistort the image points

    cam_x = camera_position[0]
    cam_y = camera_position[1]
    cam_z = camera_position[2]


    df = df._append({
        'Img_name':Img_name,
        'X_theta': x,
        'Y_theta': y,
        'Z_theta': z,
        'obj_x': tvec[0].item(),
        'obj_y': tvec[1].item(),
        'obj_z': tvec[2].item(),
        'R_cam_X_theta':p,
        'R_cam_Y_theta':q,
        'R_cam_Z_theta':r,
        'cam_x': camera_position[0].item(),
        'cam_y': camera_position[1].item(),
        'cam_z': camera_position[2].item()
    }, ignore_index=True)

# Apply the function to create a new column with numeric values
df['numeric_part'] = df['Img_name'].apply(extract_number)

print("\nSelect the direction in which the images are captured:")
print("1. Origin to End position")
print("2. End position to Origin")
dir_choice = input("Enter your choice (1 or 2): ")

if dir_choice == '1':
    df_sorted = df.sort_values(by='numeric_part').drop(columns=['numeric_part'])
elif dir_choice == '2':
    df_sorted = df.sort_values(by='numeric_part', ascending=False).drop(columns=['numeric_part'])
else:
    print("Invalid choice. Please select 1 or 2.")
# Sort the DataFrame based on the numeric part

df_sorted.to_excel('camera_extrinsic_data.xlsx', index=False)

choice = input ("\n Do you want to perform extended analysis? (y/n): ").strip().lower()
if choice == 'y':
    analysis(df_sorted,dir_choice)
else:
    print("\n Extended analysis skipped.")
    print("\n The camera extrinsic data has been saved to 'camera_extrinsic_data.xlsx'.")
    print("\n Thank you for using the camera extrinsics extraction tool!")
