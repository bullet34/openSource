import cv2
import numpy as np
import glob
import os


# ============================================================
# 설정
# ============================================================

CHECKERBOARD = (8, 5)   # 내부 코너 수
SQUARE_SIZE = 20.0      # mm

LEFT_DIR = "picture_calib/camera1_*.jpg"    # 카메라입장 좌측, 홈플래닛 
RIGHT_DIR = "picture_calib/camera2_*.jpg"   # 카메라입장 우측, 로지텍 

OUTPUT_FILE = "stereo_calibration.yaml"


# ============================================================
# 1. 체커보드 실제 3D 좌표 생성
# ============================================================

objp = np.zeros(
    (CHECKERBOARD[0] * CHECKERBOARD[1], 3),
    np.float32
)

objp[:, :2] = np.mgrid[
    0:CHECKERBOARD[0],
    0:CHECKERBOARD[1]
].T.reshape(-1, 2)

objp *= SQUARE_SIZE


# ============================================================
# 2. 이미지 목록
# ============================================================

left_images = sorted(glob.glob(LEFT_DIR))
right_images = sorted(glob.glob(RIGHT_DIR))

print("Left images :", len(left_images))
print("Right images:", len(right_images))

if len(left_images) != len(right_images):
    raise ValueError("Left/Right 이미지 개수가 다릅니다.")


# ============================================================
# 3. 코너 검출
# ============================================================

objpoints = []

imgpoints_left = []
imgpoints_right = []

image_size = None

for left_fname, right_fname in zip(left_images, right_images):

    img_left = cv2.imread(left_fname)
    img_right = cv2.imread(right_fname)

    if img_left is None:
        print("읽기 실패:", left_fname)
        continue

    if img_right is None:
        print("읽기 실패:", right_fname)
        continue

    gray_left = cv2.cvtColor(
        img_left,
        cv2.COLOR_BGR2GRAY
    )

    gray_right = cv2.cvtColor(
        img_right,
        cv2.COLOR_BGR2GRAY
    )

    if image_size is None:
        image_size = gray_left.shape[::-1]

    # -----------------------------------------
    # Left
    # -----------------------------------------

    ret_left, corners_left = cv2.findChessboardCorners(
        gray_left,
        CHECKERBOARD
    )

    # -----------------------------------------
    # Right
    # -----------------------------------------

    ret_right, corners_right = cv2.findChessboardCorners(
        gray_right,
        CHECKERBOARD
    )

    # 두 카메라 모두 성공한 경우만 사용
    if ret_left and ret_right:

        criteria = (
            cv2.TERM_CRITERIA_EPS +
            cv2.TERM_CRITERIA_MAX_ITER,
            30,
            0.001
        )

        corners_left = cv2.cornerSubPix(
            gray_left,
            corners_left,
            (11, 11),
            (-1, -1),
            criteria
        )

        corners_right = cv2.cornerSubPix(
            gray_right,
            corners_right,
            (11, 11),
            (-1, -1),
            criteria
        )

        objpoints.append(objp.copy())

        imgpoints_left.append(corners_left)
        imgpoints_right.append(corners_right)

        print(
            "OK:",
            os.path.basename(left_fname),
            os.path.basename(right_fname)
        )

        # 확인용
        cv2.drawChessboardCorners(
            img_left,
            CHECKERBOARD,
            corners_left,
            ret_left
        )

        cv2.drawChessboardCorners(
            img_right,
            CHECKERBOARD,
            corners_right,
            ret_right
        )

        cv2.imshow("Left", img_left)
        cv2.imshow("Right", img_right)

        cv2.waitKey(100)

    else:

        print(
            "FAIL:",
            os.path.basename(left_fname),
            os.path.basename(right_fname)
        )


cv2.destroyAllWindows()


# ============================================================
# 4. 이미지 개수 확인
# ============================================================

print()
print("사용된 이미지 쌍:", len(objpoints))

if len(objpoints) < 10:
    raise ValueError(
        "사용 가능한 이미지 쌍이 너무 적습니다."
    )


# ============================================================
# 5. Left 카메라 Calibration
# ============================================================

ret_left, cameraMatrix_left, distCoeffs_left, \
rvecs_left, tvecs_left = cv2.calibrateCamera(
    objpoints,
    imgpoints_left,
    image_size,
    None,
    None
)

print()
print("Left Camera Matrix")
print(cameraMatrix_left)

print()
print("Left Distortion")
print(distCoeffs_left)


# ============================================================
# 6. Right 카메라 Calibration
# ============================================================

ret_right, cameraMatrix_right, distCoeffs_right, \
rvecs_right, tvecs_right = cv2.calibrateCamera(
    objpoints,
    imgpoints_right,
    image_size,
    None,
    None
)

print()
print("Right Camera Matrix")
print(cameraMatrix_right)

print()
print("Right Distortion")
print(distCoeffs_right)


# ============================================================
# 7. Stereo Calibration
# ============================================================

stereo_criteria = (
    cv2.TERM_CRITERIA_EPS +
    cv2.TERM_CRITERIA_MAX_ITER,
    100,    # 100회
    1e-5    # 0.00001
)

flags = cv2.CALIB_FIX_INTRINSIC

ret_stereo, \
cameraMatrix_left, distCoeffs_left, \
cameraMatrix_right, distCoeffs_right, \
R, T, E, F = cv2.stereoCalibrate(

    objpoints,

    imgpoints_left,
    imgpoints_right,

    cameraMatrix_left,
    distCoeffs_left,

    cameraMatrix_right,
    distCoeffs_right,

    image_size,

    criteria=stereo_criteria,
    flags=flags
)


# ============================================================
# 8. 결과 출력
# ============================================================

print()
print("==============================")
print("Stereo Calibration Result")
print("==============================")

print()
print("R =")
print(R)

print()
print("T =")
print(T)

print()
print("Baseline (mm) =")
print(np.linalg.norm(T))

print()
print("Stereo RMS Error =")
print(ret_stereo)


# ============================================================
# 9. Stereo Rectification
# ============================================================

R1, R2, P1, P2, Q, roi_left, roi_right = cv2.stereoRectify(

    cameraMatrix_left,
    distCoeffs_left,

    cameraMatrix_right,
    distCoeffs_right,

    image_size,

    R,
    T,

    flags=cv2.CALIB_ZERO_DISPARITY,
    alpha=0
)


# ============================================================
# 10. Rectification Map 생성
# ============================================================

map1_left, map2_left = cv2.initUndistortRectifyMap(
    cameraMatrix_left,
    distCoeffs_left,
    R1,
    P1,
    image_size,
    cv2.CV_32FC1
)

map1_right, map2_right = cv2.initUndistortRectifyMap(
    cameraMatrix_right,
    distCoeffs_right,
    R2,
    P2,
    image_size,
    cv2.CV_32FC1
)


# ============================================================
# 11. YAML 저장
# ============================================================

fs = cv2.FileStorage(
    OUTPUT_FILE,
    cv2.FILE_STORAGE_WRITE
)

# 기본 정보
fs.write("image_width", image_size[0])
fs.write("image_height", image_size[1])

fs.write("checkerboard_cols", CHECKERBOARD[0])
fs.write("checkerboard_rows", CHECKERBOARD[1])
fs.write("square_size_mm", SQUARE_SIZE)

# Left
fs.write("cameraMatrix_left", cameraMatrix_left)
fs.write("distCoeffs_left", distCoeffs_left)

# Right
fs.write("cameraMatrix_right", cameraMatrix_right)
fs.write("distCoeffs_right", distCoeffs_right)

# Stereo
fs.write("R", R)
fs.write("T", T)
fs.write("E", E)
fs.write("F", F)

# Rectification
fs.write("R1", R1)
fs.write("R2", R2)
fs.write("P1", P1)
fs.write("P2", P2)
fs.write("Q", Q)

# Map
fs.write("map1_left", map1_left)
fs.write("map2_left", map2_left)
fs.write("map1_right", map1_right)
fs.write("map2_right", map2_right)

fs.release()

print()
print("저장 완료:", OUTPUT_FILE)
