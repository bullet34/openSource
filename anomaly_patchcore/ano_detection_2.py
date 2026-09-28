
### 학습 ###

import torch
from torchvision import transforms

from anomalib.data import Folder
from anomalib.models import Patchcore
from anomalib.engine import Engine


# ============================================================
# 1. 데이터 증강
# ============================================================

# train_transform = transforms.Compose([
#     # 실제 생산라인에서 약간의 위치/각도 오차가 있다고 가정
#     transforms.RandomHorizontalFlip(p=0.5),

#     transforms.RandomRotation(
#         degrees=3
#     ),

#     # 조명 차이를 어느 정도 흉내냄
#     transforms.ColorJitter(
#         brightness=0.15,
#         contrast=0.15,
#         saturation=0.05,
#         hue=0.0,
#     ),
# ])

train_transform = None

# Validation / Test에는 증강을 하지 않는 것을 권장
val_transform = None
test_transform = None


# ============================================================
# 2. DataModule
# ============================================================
datamodule = Folder(
    name="anno_product",
    root="./anno/dataset",

    normal_dir="good",
    abnormal_dir="defect",
    mask_dir="defect_mask",

    train_batch_size=16,
    eval_batch_size=16,

    num_workers=0,

    train_augmentations=train_transform,
    val_augmentations=val_transform,
    test_augmentations=test_transform,
)

# 이미지 사이즈 설정
TARGET_SIZE = (600, 600)
pre_processor = Patchcore.configure_pre_processor(
    image_size=TARGET_SIZE,
    center_crop_size=None  # 센터 크롭을 무효화하고 지정한 크기 그대로 사용
)

# ============================================================
# 3. PatchCore
# ============================================================

model = Patchcore(
    backbone="wide_resnet50_2",

    layers=[
        "layer2",
        "layer3",
    ],

    pre_processor=pre_processor,
    
    pre_trained=True,

    # 정상 feature 중 일부만 memory bank에 사용
    coreset_sampling_ratio=0.1,
)


# ============================================================
# 4. Engine
# ============================================================

engine = Engine(
    max_epochs=1,
)


# ============================================================
# 5. 학습
# ============================================================

engine.fit(
    model=model,
    datamodule=datamodule,
)


# ============================================================
# 6. 테스트
# ============================================================

engine.test(
    model=model,
    datamodule=datamodule,
)
