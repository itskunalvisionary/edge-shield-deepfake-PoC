import numpy as np
import torch
from moviepy import VideoFileClip

from models.rawnet2_arch import RawNet2Lite


class AudioPipeline:
    """
    Offline audio deepfake detection pipeline using RawNet2Lite.
    """

    def __init__(self):
        self.device = torch.device("cpu")

        self.model = RawNet2Lite()
        self.model.to(self.device)
        self.model.eval()

        self.sample_rate = 16000
        self.chunk_duration = 3  # seconds
        self.chunk_size = self.sample_rate * self.chunk_duration

    def _extract_audio(self, video_path):
        clip = VideoFileClip(video_path)
        audio = clip.audio.to_soundarray(fps=self.sample_rate)
        clip.close()

        # Convert to mono
        if audio.ndim == 2:
            audio = audio.mean(axis=1)

        return audio.astype(np.float32)

    def process(self, video_path):
        waveform = self._extract_audio(video_path)

        # Normalize waveform
        waveform = waveform / (np.max(np.abs(waveform)) + 1e-9)

        scores = []

        with torch.no_grad():
            for i in range(0, len(waveform), self.chunk_size):
                chunk = waveform[i : i + self.chunk_size]

                if len(chunk) < self.chunk_size:
                    continue

                tensor = torch.tensor(chunk).unsqueeze(0).unsqueeze(0)
                tensor = tensor.to(self.device)

                output = self.model(tensor)
                score = torch.sigmoid(output).item()
                scores.append(score)

        if not scores:
            # No reliable audio evidence → neutral uncertainty
            return 0.5

        mean_score = float(np.mean(scores))

        # 🔹 PoC confidence bucketing (same logic as video)
        if mean_score < 0.45:
            return 0.25      # Likely REAL voice
        elif mean_score > 0.55:
            return 0.75      # Likely FAKE voice
        else:
            return 0.5       # Uncertain / novel generation

