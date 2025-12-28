import torch
import torch.nn as nn
import torch.nn.functional as F


class RawNet2Lite(nn.Module):
    """
    RawNet2-style lightweight audio spoof detection model
    Input : raw waveform (B, 1, T)
    Output: single logit (spoof probability after sigmoid)
    """

    def __init__(self):
        super().__init__()

        self.block1 = nn.Sequential(
            nn.Conv1d(1, 64, kernel_size=3, stride=3, padding=1),
            nn.BatchNorm1d(64),
            nn.ReLU()
        )

        self.block2 = nn.Sequential(
            nn.Conv1d(64, 128, kernel_size=3, stride=3, padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU()
        )

        self.block3 = nn.Sequential(
            nn.Conv1d(128, 256, kernel_size=3, stride=3, padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU()
        )

        self.pool = nn.AdaptiveAvgPool1d(1)
        self.fc = nn.Linear(256, 1)

    def forward(self, x):
        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)

        x = self.pool(x).squeeze(-1)
        return self.fc(x)
