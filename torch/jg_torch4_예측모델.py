import torch
import torch.nn as nn
import random, os

os.system('cls')


# a = [random.randint(0, 2) for _ in range(0, 3)]

result = []

# for i in range(0, 6):   # 샘플
#     semi_result = []
#     for j in range(0, 3):   # 시퀀스
#         a = [random.randint(0, 2), random.randint(6, 8), random.randint(12, 14)]    # 특징
#         semi_result.append(a)
#     result.append(semi_result)
    
# a = torch.tensor(result, dtype=torch.float32)   # 텐서(실수) 변환

for i in range(0, 10):
    semi_result = []
    for j in range(0, 7):
        third_result = []
        new_dt1 = random.randint(1, 12)
        for k in range(new_dt1, new_dt1+10):
            third_result.append(k)
        semi_result.append(third_result)
    result.append(semi_result)

a = torch.tensor(result, dtype=torch.float32)   # 텐서(실수) 변환

##
result2 = []

# for i in range(0, 6):
#     b = [random.randint(0, 2), random.randint(6, 8), random.randint(12, 14)]
#     result2.append(b)

for i in range(0, 10):
    new_dt1 = random.randint(1, 12)
    b = [i for i in range(new_dt1, new_dt1+10)]
    result2.append(b)
    
b = torch.tensor(result2, dtype=torch.float32)

##
# LSTM 모델 정의
class LSTMModel(nn.Module):
    def __init__(self,
                 input_size=10,  # 한 시점의 입력 feature 수
                 hidden_size=32,    # LSTM 내부 기억 공간 크기
                 num_layers=2,  # LSTM 층 수 - 데이터 많고 패턴이 복잡 자연어처리 음성인식 층수 늘린다
                 output_size=10):    # 다음 시점의 feature 3개 예측
        super().__init__()

        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers, 
            batch_first=True
        )

        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])   # 마지막 시점의 출력 사용
        return out

# 모델 생성
model = LSTMModel()

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# 학습
epochs = 200

for epoch in range(epochs):

    model.train()

    # 예측
    pred = model(a)

    # 손실 계산
    loss = criterion(pred, b)

    # Gradient 초기화
    optimizer.zero_grad()

    # 역전파
    loss.backward()

    # 가중치 업데이트
    optimizer.step()

    # if (epoch + 1) % 50 == 0:
    print(f"Epoch {epoch+1:3d}, Loss = {loss.item():.6f}")

# 모델 저장
torch.save(model.state_dict(), "lstm_model.pth")
