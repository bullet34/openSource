from ultralytics import YOLO

model = YOLO("yolov8n.pt")

# model.train(
#     data="data.yaml",
#     epochs=100,
#     imgsz=640,
#     batch=16
# )

# 추가설정
# model.train(
#     data="data.yaml",
#     epochs=100,
#     imgsz=640,
#     degrees=10,
#     translate=0.1,
#     scale=0.5
# )


model.train(
    data="./dataset/data.yaml",
    epochs=50,
    freeze=10
)
