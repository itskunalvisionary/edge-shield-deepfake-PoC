import torch
import torch.nn as nn
import timm


class XceptionNet(nn.Module):
    """
    Xception-based CNN for deepfake detection
    Compatible with xception_deepfake.pth
    CPU-safe, edge-deployable
    """

    def __init__(self, num_classes=1):
        super().__init__()

        # True Xception backbone
        self.backbone = timm.create_model(
            "xception",
            pretrained=False,
            num_classes=0,      # remove classifier
            global_pool="avg"
        )

        in_features = self.backbone.num_features
        self.classifier = nn.Linear(in_features, num_classes)

    def forward(self, x):
        x = self.backbone(x)
        return self.classifier(x)
