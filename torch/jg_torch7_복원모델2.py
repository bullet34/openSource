import torch
import torch.nn as nn

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class LSTMAutoEncoder(nn.Module):

    def __init__(self,
                 input_dim,
                 hidden_dim,
                 latent_dim,
                 num_layers=1):

        super().__init__()

        self.encoder = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True
        )

        self.fc_enc = nn.Linear(hidden_dim, latent_dim)

        self.fc_dec = nn.Linear(latent_dim, hidden_dim)

        self.decoder = nn.LSTM(
            input_size=hidden_dim,
            hidden_size=input_dim,
            num_layers=num_layers,
            batch_first=True
        )

    def forward(self, x):

        batch_size = x.size(0)
        seq_len = x.size(1)

        _, (hidden, _) = self.encoder(x)

        latent = self.fc_enc(hidden[-1])

        hidden_dec = self.fc_dec(latent)

        decoder_input = hidden_dec.unsqueeze(1).repeat(1, seq_len, 1)

        output, _ = self.decoder(decoder_input)

        return output


INPUT_DIM = 8
HIDDEN_DIM = 64
LATENT_DIM = 16

model = LSTMAutoEncoder(
    INPUT_DIM,
    HIDDEN_DIM,
    LATENT_DIM
).to(device)

criterion = nn.MSELoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=1e-3
)
