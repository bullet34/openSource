import torch
import torch.nn as nn


class LSTMAutoEncoder(nn.Module):

    def __init__(self,
                 input_size=3,
                 hidden_size=64):

        super().__init__()

        # Encoder
        self.encoder = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            batch_first=True
        )


        # Decoder
        self.decoder = nn.LSTM(
            input_size=hidden_size,
            hidden_size=hidden_size,
            batch_first=True
        )


        # hidden -> 원래 feature 개수로 복원
        self.fc = nn.Linear(
            hidden_size,
            input_size
        )


    def forward(self, x):

        # =====================
        # Encoder
        # =====================

        _, (hidden, cell) = self.encoder(x)


        # 마지막 hidden을 사용
        # shape:
        # (1, batch, hidden)
        

        # =====================
        # Decoder 입력 생성
        # =====================

        seq_len = x.size(1)


        decoder_input = hidden.permute(1,0,2)

        # (batch,1,hidden)


        # sequence 길이만큼 복사

        decoder_input = decoder_input.repeat(
            1,
            seq_len,
            1
        )

        # (batch,seq_len,hidden)



        # =====================
        # Decoder
        # =====================

        output, _ = self.decoder(
            decoder_input,
            (hidden, cell)
        )


        # hidden -> feature 복원

        reconstructed = self.fc(output)


        return reconstructed
    
##


# 모델 생성
model = LSTMAutoEncoder()

criterion = nn.MSELoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)

# 학습
epochs = 500


for epoch in range(epochs):

    model.train()


    reconstructed = model(a)


    # 입력과 복원 결과 비교
    loss = criterion(
        reconstructed,
        a
    )


    optimizer.zero_grad()

    loss.backward()

    optimizer.step()


    if (epoch+1)%50 == 0:
        print(
            epoch+1,
            loss.item()
        )
        
# 오차 확인 데이터 생성
new_data = torch.tensor([
    [
        [0,6,12],
        [1,7,13],
        [2,8,14]
    ]
], dtype=torch.float32)

# 모델 실행
model.eval()

with torch.no_grad():

    output = model(new_data)


    error = torch.mean(
        (output - new_data)**2
    )


print(error.item())
