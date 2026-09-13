import cv2

# 마커를 저장할 리스트
markers = []


def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        markers.append((x, y))
        print(f"마커 추가: ({x}, {y})")


# cap = cv2.VideoCapture(0)

cv2.namedWindow("Camera")
cv2.setMouseCallback("Camera", mouse_callback)

img = cv2.imread("picture_calib/camera2_21.jpg")
while True:
    frame = img.copy()


    # 저장된 모든 마커 표시
    for i, (x, y) in enumerate(markers):
        cv2.rectangle(frame, (x-20,y-20), (x+20,y+20), (255,0,0), 2)
        
        # 원형 마커
        cv2.circle(frame, (x, y), 8, (0, 0, 255), -1)
        

        # 십자 표시
        cv2.drawMarker(
            frame,
            (x, y),
            (0, 255, 0),
            markerType=cv2.MARKER_CROSS,
            markerSize=20,
            thickness=2
        )

        # 마커 번호
        cv2.putText(
            frame,
            f"M{i + 1} ({x}, {y})",
            (x + 15, y - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(30) & 0xFF

    # ESC -> 종료
    if key == 27:
        break

    # R -> 마커 전체 삭제
    elif key == ord("r"):
        markers.clear()
        print("마커 삭제")


cv2.destroyAllWindows()
