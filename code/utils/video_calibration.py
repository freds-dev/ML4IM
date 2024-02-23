import cv2
import numpy as np
from utils.paths import get_calib_rgb, get_calib_event, get_homography


# Ihr hattet eure utils nicht mitgeschickt, habt das aber wahrscheinlich ziemlich genauso gemacht?
def read_calibration(calib_path):
    calib = cv2.FileStorage(calib_path, cv2.FILE_STORAGE_READ)
    mat = calib.getNode("K").mat()
    dist = calib.getNode("D").mat()
    calib.release()
    return mat, dist


def undistort_img(img, is_event = True, alpha = 1.0):
    if is_event:
        mat, dist = read_calibration(get_calib_event())
    else:
        mat, dist = read_calibration(get_calib_rgb())
    
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
        mat, dist, img.shape[:2], alpha, img.shape[:2])
    return cv2.undistort(img, mat, dist, None, newcameramtx), newcameramtx

def translate_img(img, height, width, x = 0, y = 12):
    calibration_file = get_homography()
    fs = cv2.FileStorage(calibration_file, cv2.FILE_STORAGE_READ)
    homography_matrix = fs.getNode('H').mat()
    homography_matrix = homography_matrix @ np.array([ [1, 0, x], [0, 1, y], [0, 0, 1] ], dtype=np.float32)
    fs.release()
    return cv2.warpPerspective(img,homography_matrix,(height,width), flags=cv2.WARP_INVERSE_MAP)
    