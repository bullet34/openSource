import cv2
import numpy as np

# 이미지상의 점
image_points = np.float32([
    [120, 80],
    [520, 100],
    [560, 450],
    [80, 420],
    [300, 200],
    [400, 250],
    [200, 300],
    [450, 350],
    [250, 400],
    [350, 450]
])

# 각 점에 대응하는 실제 좌표
world_points = np.float32([
    [0.0, 0.0],
    [4.0, 0.0],
    [4.0, 6.0],
    [0.0, 6.0],
    [1.5, 2.0],
    [2.7, 2.5],
    [1.0, 3.0],
    [3.2, 4.0],
    [1.8, 4.5],
    [2.8, 5.2]
])

# Homography 계산
H, mask = cv2.findHomography(
    image_points,
    world_points,
    cv2.RANSAC
)

print(H)

### 좌표변환 ###

point = np.float32([
    [[350, 300]]
])

world_point = cv2.perspectiveTransform(
    point,
    H
)

print(world_point)
print(world_point[0][0][0])
