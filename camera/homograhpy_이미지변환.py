import cv2
import numpy as np

# 이미지 불러오기
img = cv2.imread("picture_calib/camera1_16.jpg")
points = []


# 마우스 클릭 함수
def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
        points.append([x, y])
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        cv2.putText(
            img, str(len(points)),
            (x + 10, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7, (0, 255, 0), 2
        )


cv2.namedWindow("Image")
cv2.setMouseCallback("Image", click)

print("정면으로 펴고 싶은 영역의 네 꼭짓점을 클릭하세요.")
print("순서: 좌상 → 우상 → 우하 → 좌하")
print("4점을 선택한 후 Enter를 누르세요.")
print("ESC를 누르면 종료합니다.")

while True:
    cv2.imshow("Image", img)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:       # ESC
        break

    if key == 13 and len(points) == 4:   # Enter
        break


cv2.destroyAllWindows()


# 4점이 선택되지 않았으면 종료
if len(points) != 4:
    print("4개의 점을 선택하지 않았습니다.")
    exit()


# ---------------------------------------------------------
# Homography
# ---------------------------------------------------------

src = np.float32(points)

# 결과 이미지 크기
width = 640
height = 480

# 정면으로 펴진 이미지의 네 꼭짓점
dst = np.float32([
    [0, 0],
    [width, 0],
    [width, height],
    [0, height]
])

# Homography 행렬 계산
H = cv2.getPerspectiveTransform(src, dst)

# Perspective Transform
result = cv2.warpPerspective(
    img,
    H,
    (width, height)
)


# 결과 저장
cv2.imwrite("homogrhapy_result1.jpg", result)

# 결과 확인
cv2.imshow("Result", result)

print("변환 완료!")
print("result.jpg 로 저장되었습니다.")

cv2.waitKey(0)
cv2.destroyAllWindows()
