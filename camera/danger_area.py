import cv2
import numpy as np
from ultralytics import YOLO


model = YOLO("yolov8n.pt")
# print(model.names)
cap = cv2.VideoCapture(0)

# 위험 구역 좌표 설정
roi_pts = np.array([
    [500, 450], 
    [800, 450], 
    [900, 550], 
    [400, 550]
], dtype=np.int32)

# 파라미터 - 이미지, 위험구역 좌표, 위험 판별 인자
def draw_transparent_roi(frame, roi_polygon, danger):
  
    # 원본 프레임을 복사
    overlay = frame.copy()  
    
    if danger:
        cv2.fillPoly(overlay, [roi_polygon], (0, 0, 255))   # 위험 구역
    else:
        cv2.fillPoly(overlay, [roi_polygon], (0, 255, 0))  # 안전 구역

        
    # 투명도 설정 (alpha 값: 0.0 ~ 1.0, 숫자가 낮을수록 투명해짐, 예: 0.4는 40% 불투명)
    alpha = 0.1
    
    # 원본 프레임과 오버레이 도화지 합치기 (알파 블렌딩)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    
    # 구역의 경계선을
    # cv2.polylines(frame, [roi_polygon], isClosed=True, color=(0, 0, 255), thickness=2)
    
    return frame

### 메인 ###
while True:
    
    ret, frame = cap.read()

    if not ret:
        print("프레임을 받아올 수 없습니다.")
        break
    
    # 클래스 0번 person
    result = model.predict(source=frame, classes=[0], verbose=False)
    
    # 위험구역 판별 변수
    is_danger = False
    
    # 바운딩 박스 좌표(하단 우측, 중앙, 좌측)
    boxes = result[0].boxes.xyxy
    for box in boxes:
        xmin, ymin, xmax, ymax = box
        xy = (int((xmin+xmax)/2), int(ymax))
        xy1 = (int(xmin), int(ymax))
        xy2 = (int(xmax), int(ymax))
        
        # 중앙좌표 점
        cv2.circle(frame, xy, 3, (0, 0, 0), -1)
        
        dg_result1 = cv2.pointPolygonTest(roi_pts, xy, False)
        dg_result2 = cv2.pointPolygonTest(roi_pts, xy1, False)
        dg_result3 = cv2.pointPolygonTest(roi_pts, xy2, False)
        
        if (dg_result1 >= 0 or dg_result2 >= 0 or dg_result3 >= 0):
            is_danger = True
    
    # 위험구역 그리기
    danger_area_frame = draw_transparent_roi(frame, roi_pts, is_danger)
    
    result[0].orig_img = danger_area_frame

    # plot()을 호출하면 ROI 구역 위에 바운딩 박스가 그려짐
    # 최종 이미지
    result_frame = result[0].plot()
    
    cv2.imshow("Live", result_frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()


