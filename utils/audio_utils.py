import torchaudio
import torch
from config.settings import AUDIO_SAMPLE_RATE, MAX_AUDIO_DURATION


def load_audio(audio_path):
    """
    Loads and standardizes audio waveform.
    """
    waveform, sample_rate = torchaudio.load(audio_path)

    # Convert to mono if stereo
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)

    # Resample if needed
    if sample_rate != AUDIO_SAMPLE_RATE:
        resampler = torchaudio.transforms.Resample(
            orig_freq=sample_rate,
            new_freq=AUDIO_SAMPLE_RATE
        )
        waveform = resampler(waveform)

    # Trim to max duration
    max_samples = AUDIO_SAMPLE_RATE * MAX_AUDIO_DURATION
    waveform = waveform[:, :max_samples]

    return waveform
