import torch
import torch.nn as nn
import random, os
from jg_torch4_예측모델 import LSTMModel

os.system('cls')

# 테스트 데이터
result = [] 
# for i in range(0, 3):
#     b = [random.randint(0, 2), random.randint(6, 8), random.randint(12, 14)]
#     result.append(b)
##
# for i in range(0, 7):
#     new_dt1 = random.randint(1, 12)
#     b = [i for i in range(new_dt1, new_dt1+10)]
#     result.append(b)
##
new_dt1 = random.randint(1, 12)
b = [i for i in range(new_dt1, new_dt1+10)]
result.append(b)
    
b = torch.tensor(result, dtype=torch.float32)
print(f'변환전: {b}')
b = b.unsqueeze(0)

print(f'테스트 데이터: {b}')

# 모델 불러오기
model = LSTMModel()

model.load_state_dict(torch.load("lstm_model.pth"))
model.eval()

# 예측
with torch.no_grad():
    pred = model(b)

print(pred)
