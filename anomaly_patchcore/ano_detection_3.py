
### 판정 - 히트맵 max value ###

import torch
from torchvision import transforms

from anomalib.data import Folder
from anomalib.models import Patchcore
from anomalib.engine import Engine
import glob

import matplotlib.pyplot as plt
import numpy as np

checkpoint_path = (
    "./results/Patchcore/anno_product/latest/weights/lightning/model.ckpt"
)


# ============================================================
# 학습된 checkpoint 불러오기
# ============================================================

model = Patchcore.load_from_checkpoint(
    checkpoint_path,
    backbone="wide_resnet50_2",
    layers=[
        "layer2",
        "layer3",
    ],
    weights_only=False,
    pre_trained=True,
    coreset_sampling_ratio=0.1,
)


# ============================================================
# Engine
# ============================================================

engine = Engine()


# ============================================================
# 검사할 이미지
# ============================================================

image_path = "C:/Users/bulle/test_py/anno/dataset/test/p2.jpg"
# image_paths = glob.glob("./test_images/*.jpg")


# ============================================================
# Prediction
# ============================================================

predictions = engine.predict(
    model=model,
    data_path=image_path,
)


# ============================================================
# 결과 출력
# ============================================================

for prediction in predictions:

    score = float(prediction.pred_score)
    label = int(prediction.pred_label)

    if label == 0:
        result = "정상"
    else:
        result = "불량"

    print("--------------------------------")
    print(f"이미지 : {image_path}")
    print(f"Anomaly Score : {score:.4f}")
    print(f"판정 : {result}")
    print("--------------------------------")

    
    # 1. 원본 이미지 처리 (배치 차원 제거 및 채널 순서 변경: (C, H, W) -> (H, W, C))
    img = prediction.image
    if hasattr(img, "cpu"):
        img = img.cpu().numpy()
    
    img = np.squeeze(img) # (1, 3, 256, 256) -> (3, 256, 256)
    if img.ndim == 3 and img.shape[0] in [1, 3]:
        img = np.transpose(img, (1, 2, 0)) # (3, 256, 256) -> (256, 256, 3)

    # 만약 값이 0~1 사이의 float형태가 아니라면 픽셀 범위 확인을 위해 스케일링이 필요할 수 있습니다.
    # 만약 이미지가 하얗게 나온다면 img = np.clip(img, 0, 1) 등을 적용해볼 수 있습니다.

    # 2. 히트맵 처리
    anomaly_map = prediction.anomaly_map
    if hasattr(anomaly_map, "cpu"):
        anomaly_map = anomaly_map.cpu().numpy()
    anomaly_map = np.squeeze(anomaly_map) # 차원 정리

    print("--------------------------------")
    raw_score_max = float(np.max(anomaly_map))
    print(f"Raw Score (Map Max Value) : {raw_score_max:.4f}")
    print("--------------------------------")
    
    # 3. Matplotlib으로 시각화 (원본 vs 히트맵)
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # 원본 이미지 출력
    axes[0].imshow(img)
    axes[0].set_title(f"Original Image\n({result})")
    axes[0].axis("off")

    # 히트맵 오버레이 출력
    axes[1].imshow(img)
    im = axes[1].imshow(anomaly_map, cmap="jet", alpha=0.5)  
    axes[1].set_title(f"Anomaly Heatmap\nScore: {score:.4f}")
    axes[1].axis("off")

    # 컬러바 추가
    fig.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04)

    plt.tight_layout()
    plt.show()
