
### 데이터 증강 ###

import matplotlib.pyplot as plt
from PIL import Image
from torchvision import transforms

image_path = "./anno/p2.jpg"

image = Image.open(image_path).convert("RGB")

# 모델 입력 크기 확인
resize = transforms.Resize((640, 640))

# 학습 증강
train_transform = transforms.Compose([
    # transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(degrees=3),
    transforms.ColorJitter(
        brightness=0.15,
        contrast=0.15,
    ),
])

fig, axes = plt.subplots(5, 5, figsize=(12, 9))

for i, ax in enumerate(axes.flat):
    # 먼저 256x256으로 변환
    resized = resize(image)

    # 증강
    if i == 0:
        # 첫 번째는 원본
        ax.imshow(image)
        ax.set_title("Original")
    else:
        augmented = train_transform(resized)
        ax.imshow(augmented)
        ax.set_title(f"Augmented {i}")
        augmented.save(f"C:/Users/bulle/test_py/anno/dataset/good/good_{i}.jpg")

    ax.axis("off")

plt.tight_layout()
plt.show()
