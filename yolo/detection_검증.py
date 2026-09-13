from ultralytics import YOLO

model = YOLO("best.pt")

# 추론
result = model.predict("test.jpg")


# 모델평가
metrics = model.val(
    data="dataset/data.yaml",
    split="test"
)
