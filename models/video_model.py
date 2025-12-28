import torch
import numpy as np
import cv2
import timm


class VideoDeepfakeModel:
    """
    Option B-1:
    Uses TIMM's pretrained Xception backbone (ImageNet)
    to avoid architecture–weight mismatch.
    """

    def __init__(self):
        self.device = torch.device("cpu")

        # ✅ TIMM Xception (fully compatible, no missing keys)
        self.model = timm.create_model(
            "xception",
            pretrained=True,
            num_classes=1
        )

        self.model.to(self.device)
        self.model.eval()

        # ImageNet normalization (REQUIRED)
        self.mean = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
        self.std = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)

    def preprocess(self, face_frame):
        face_frame = cv2.resize(face_frame, (224, 224))

        tensor = torch.tensor(face_frame, dtype=torch.float32)
        tensor = tensor.permute(2, 0, 1).unsqueeze(0) / 255.0
        tensor = (tensor - self.mean) / self.std

        return tensor.to(self.device)

    def predict(self, face_frames):
        """
        Produces a real-valued confidence score.
        Variance is now meaningful because model is alive.
        """

        if not face_frames:
            return 0.5

        scores = []

        with torch.no_grad():
            for frame in face_frames:
                output = self.model(self.preprocess(frame))
                score = torch.sigmoid(output).item()
                scores.append(score)

        if len(scores) < 5:
            return 0.5

        mean_score = float(np.mean(scores))
        std_score = float(np.std(scores))

        print(f"[VideoModel] mean={mean_score:.3f}, std={std_score:.3f}")

        # Optional variance hint (kept simple)
        return mean_score
