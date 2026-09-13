import cv2
import numpy as np


# ============================================================
# 설정
# ============================================================

CALIBRATION_FILE = "stereo_calibration.yaml"

LEFT_IMAGE = "picture_calib/camera1_23.jpg"
RIGHT_IMAGE = "picture_calib/camera2_23.jpg"


# ============================================================
# 1. Calibration 데이터 불러오기
# ============================================================

fs = cv2.FileStorage(
    CALIBRATION_FILE,
    cv2.FILE_STORAGE_READ
)

if not fs.isOpened():
    raise RuntimeError(
        f"Calibration 파일을 열 수 없습니다: {CALIBRATION_FILE}"
    )


cameraMatrix_left = fs.getNode(
    "cameraMatrix_left"
).mat()

distCoeffs_left = fs.getNode(
    "distCoeffs_left"
).mat()

cameraMatrix_right = fs.getNode(
    "cameraMatrix_right"
).mat()

distCoeffs_right = fs.getNode(
    "distCoeffs_right"
).mat()


R1 = fs.getNode("R1").mat()
R2 = fs.getNode("R2").mat()

P1 = fs.getNode("P1").mat()
P2 = fs.getNode("P2").mat()

Q = fs.getNode("Q").mat()


map1_left = fs.getNode(
    "map1_left"
).mat()

map2_left = fs.getNode(
    "map2_left"
).mat()

map1_right = fs.getNode(
    "map1_right"
).mat()

map2_right = fs.getNode(
    "map2_right"
).mat()


fs.release()


# ============================================================
# 2. 이미지 읽기
# ============================================================

img_left = cv2.imread(LEFT_IMAGE)
img_right = cv2.imread(RIGHT_IMAGE)


if img_left is None:
    raise RuntimeError(
        f"Left 이미지를 읽을 수 없습니다: {LEFT_IMAGE}"
    )

if img_right is None:
    raise RuntimeError(
        f"Right 이미지를 읽을 수 없습니다: {RIGHT_IMAGE}"
    )


# ============================================================
# 3. 이미지 크기 확인
# ============================================================

if img_left.shape[:2] != img_right.shape[:2]:
    raise RuntimeError(
        "Left와 Right 이미지의 해상도가 다릅니다."
    )


image_size = (
    img_left.shape[1],
    img_left.shape[0]
)

print("Image size:", image_size)


# ============================================================
# 4. Calibration 정보 출력
# ============================================================

print()
print("==============================")
print("Calibration Information")
print("==============================")

print("T =")
print(fs if False else "YAML에서 로드 완료")

print()
print("P1 =")
print(P1)

print()
print("P2 =")
print(P2)

print()
print("Q =")
print(Q)


# ============================================================
# 5. Rectification
# ============================================================

rect_left = cv2.remap(
    img_left,
    map1_left,
    map2_left,
    cv2.INTER_LINEAR
)

rect_right = cv2.remap(
    img_right,
    map1_right,
    map2_right,
    cv2.INTER_LINEAR
)


# ============================================================
# 6. Rectification 결과 확인
# ============================================================

h, w = rect_left.shape[:2]

combined = np.hstack([
    rect_left,
    rect_right
])


for y in range(0, h, 50):

    cv2.line(
        combined,
        (0, y),
        (2 * w, y),
        (0, 255, 0),
        1
    )


cv2.imshow(
    "Rectified Left + Right",
    combined
)

print()
print("Rectification 화면")
print("수평선이 좌/우 영상에서 정확히 맞는지 확인하세요.")
print("아무 키나 누르면 다음 단계로 진행합니다.")

cv2.waitKey(0)
cv2.destroyAllWindows()


# ============================================================
# 7. Gray Scale
# ============================================================

gray_left = cv2.cvtColor(
    rect_left,
    cv2.COLOR_BGR2GRAY
)

gray_right = cv2.cvtColor(
    rect_right,
    cv2.COLOR_BGR2GRAY
)


# ============================================================
# 8. StereoSGBM
# ============================================================

min_disparity = 0

# 기존 128 → 512로 증가
num_disparities = 16 * 48

block_size = 5


stereo = cv2.StereoSGBM_create(

    minDisparity=min_disparity,

    numDisparities=num_disparities,

    blockSize=block_size,

    P1=8 * block_size * block_size,

    P2=32 * block_size * block_size,

    disp12MaxDiff=1,

    uniquenessRatio=10,

    speckleWindowSize=100,

    speckleRange=2,

    preFilterCap=63,

    mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
)


# ============================================================
# 9. Disparity 계산
# ============================================================

disparity = stereo.compute(
    gray_left,
    gray_right
).astype(np.float32) / 16.0


# ============================================================
# 10. 유효한 Disparity 확인
# ============================================================

valid_disparity = (
    np.isfinite(disparity) &
    (disparity > min_disparity)
)


valid_count = np.count_nonzero(
    valid_disparity
)

total_count = disparity.size

valid_ratio = (
    valid_count / total_count * 100
)


print()
print("==============================")
print("Disparity Information")
print("==============================")

print(
    f"Valid pixels : {valid_count} / {total_count}"
)

print(
    f"Valid ratio  : {valid_ratio:.2f}%"
)


if valid_count > 0:

    disp_min = disparity[
        valid_disparity
    ].min()

    disp_max = disparity[
        valid_disparity
    ].max()

    print(
        f"Disparity min: {disp_min:.4f}"
    )

    print(
        f"Disparity max: {disp_max:.4f}"
    )

else:

    print("유효한 disparity가 없습니다.")


# ============================================================
# 11. Disparity 화면
# ============================================================

disp_display = np.zeros_like(
    disparity,
    dtype=np.uint8
)


if valid_count > 0:

    # 유효한 값만 표시
    disp_normalized = cv2.normalize(
        disparity,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    disp_display[
        valid_disparity
    ] = disp_normalized[
        valid_disparity
    ].astype(np.uint8)


cv2.imshow(
    "Disparity",
    disp_display
)

print()
print("Disparity 화면")
print("아무 키나 누르면 다음 단계로 진행합니다.")

cv2.waitKey(0)
cv2.destroyAllWindows()


# ============================================================
# 12. Disparity → 3D
# ============================================================

points_3d = cv2.reprojectImageTo3D(
    disparity,
    Q
)


# ============================================================
# 13. 중앙 픽셀 Depth
# ============================================================

x = w // 2
y = h // 2

disparity_value = disparity[y, x]


print()
print("==============================")
print("Center Point")
print("==============================")

print(
    f"Pixel: ({x}, {y})"
)

print(
    f"Disparity: {disparity_value:.4f}"
)


if disparity_value > 0:

    X, Y, Z = points_3d[y, x]

    print()
    print("3D:")
    print(f"X = {X:.2f} mm")
    print(f"Y = {Y:.2f} mm")
    print(f"Z = {Z:.2f} mm")

else:

    print(
        "중앙 픽셀의 disparity가 유효하지 않습니다."
    )


# ============================================================
# 14. 여러 위치 Depth
# ============================================================

points = [
    (w // 2, h // 2),
    (w // 4, h // 2),
    (w * 3 // 4, h // 2),
    (w // 2, h // 4),
    (w // 2, h * 3 // 4),
]


print()
print("==============================")
print("Depth Samples")
print("==============================")


for x, y in points:

    disparity_value = disparity[y, x]

    print(
        f"Pixel ({x}, {y}) "
        f"Disparity={disparity_value:.2f}",
        end=" "
    )


    # 유효하지 않은 disparity
    if (
        not np.isfinite(disparity_value)
        or disparity_value <= 0
    ):

        print("Depth=INVALID")
        continue


    X, Y, Z = points_3d[y, x]


    # 비정상적인 Z 방지
    if (
        not np.isfinite(Z)
        or Z <= 0
    ):

        print("Depth=INVALID")
        continue


    print(
        f"Depth Z={Z:.2f} mm"
    )


# ============================================================
# 15. 유효한 disparity 중 하나를 자동으로 찾아서 Depth 출력
# ============================================================

print()
print("==============================")
print("Example Valid 3D Point")
print("==============================")


ys, xs = np.where(
    valid_disparity
)


if len(xs) > 0:

    # 화면 중앙에 가까운 유효 픽셀을 찾음
    center_x = w // 2
    center_y = h // 2


    distances = (
        (xs - center_x) ** 2 +
        (ys - center_y) ** 2
    )


    index = np.argmin(
        distances
    )


    x = xs[index]
    y = ys[index]


    disparity_value = disparity[
        y,
        x
    ]


    X, Y, Z = points_3d[
        y,
        x
    ]


    print(
        f"Pixel: ({x}, {y})"
    )

    print(
        f"Disparity: {disparity_value:.2f}"
    )

    print(
        f"X = {X:.2f} mm"
    )

    print(
        f"Y = {Y:.2f} mm"
    )

    print(
        f"Z = {Z:.2f} mm"
    )

else:

    print(
        "유효한 3D 점을 찾을 수 없습니다."
    )


# ============================================================
# 16. 종료
# ============================================================

cv2.destroyAllWindows()
