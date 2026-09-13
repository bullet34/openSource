import cv2
import numpy as np
import glob

CHECKERBOARD = (8, 5)
SQUARE_SIZE = 20.0   # mm

objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)

objp[:, :2] = np.mgrid[
    0:CHECKERBOARD[0],
    0:CHECKERBOARD[1]
].T.reshape(-1, 2)

objp *= SQUARE_SIZE # objp, 체커보드 실제 좌표

##

objpoints = []   # 실제 좌표
imgpoints = []   # 이미지 좌표

images = glob.glob("open/*.jpg")

for fname in images:

    img = cv2.imread(fname)
    print(fname, img is None)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    # 1채널 그레이 이미지 변환

    ret, corners = cv2.findChessboardCorners(   # 이미지상의 체커보드 코너 검출(좌표 검출)
        gray,
        CHECKERBOARD
    )

    if ret:

        corners = cv2.cornerSubPix( # 좌표 소수점단위 정밀 검출
            gray,
            corners,
            (11,11),
            (-1,-1),
            (
                cv2.TERM_CRITERIA_EPS +     # 계산 30회 또는 계산 결과의 변화가 0.001 이하일 때까지 
                cv2.TERM_CRITERIA_MAX_ITER,
                30,
                0.001
            )
        )
        
        objpoints.append(objp)  # 이미지 한개의 체커보드 실제 좌표들 저장
        imgpoints.append(corners)   # 이미지 한개의 체커보드 이미지 좌표들 저장

        cv2.drawChessboardCorners(  # 이미지에 체커보드 그려서 화면에 띄워주기
            img,
            CHECKERBOARD,
            corners,
            ret
        )
        cv2.imshow("Corners", img)
        cv2.waitKey(100)

cv2.destroyAllWindows() # 띄운 이미지 닫기
        
###

ret, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(  # 각각의 이미지에 대한 체커보드 실제좌표와 이미지 좌표를 토대로 캘리브레이션 
    objpoints,                                                      # cameraMatrix 이미지 투영 내부파라미터, distCoeffs 렌즈왜곡계수, rvecs 체커보드 회전방향, tvecs 체커보드 위치
    imgpoints,                                                      # ret 재투영오차, ex) 0.53 = 0.53 픽셀 오차 
    gray.shape[::-1],
    None,
    None
)
print(ret)
img = cv2.imread("picture_calib/camera2_21.jpg")

undistorted = cv2.undistort(    # 왜곡 보정 이미지
    img,
    cameraMatrix,
    distCoeffs
)

cv2.imshow("Original", img)
cv2.imshow("Undistorted", undistorted)
print(gray.shape)
cv2.waitKey(0)


##save
# fs = cv2.FileStorage(
#     "camera_calibration.yaml",
#     cv2.FILE_STORAGE_WRITE
# )

# fs.write("cameraMatrix", cameraMatrix)
# fs.write("distCoeffs", distCoeffs)

# fs.release()

##load
# fs = cv2.FileStorage(
#     "camera_calibration.yaml",
#     cv2.FILE_STORAGE_READ
# )

# cameraMatrix = fs.getNode("cameraMatrix").mat()
# distCoeffs = fs.getNode("distCoeffs").mat()

# fs.release()
