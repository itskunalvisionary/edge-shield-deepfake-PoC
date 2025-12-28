# ==============================
# VIDEO PIPELINE SETTINGS
# ==============================

VIDEO_FRAME_SIZE = 224        # Model input size
FRAME_SAMPLE_RATE = 10        # Process every Nth frame

# Haar Cascade path
FACE_CASCADE_PATH = (
    "assets/haarcascades/haarcascade_frontalface_default.xml"
)

# Safety checks
MIN_FACE_SIZE = 60            # Ignore tiny detections

# ==============================
# VIDEO MODEL SETTINGS
# ==============================

VIDEO_MODEL_WEIGHTS = "models/weights/xception_deepfake.pth"
VIDEO_FAKE_THRESHOLD = 0.6

# ==============================
# AUDIO PIPELINE SETTINGS
# ==============================

AUDIO_SAMPLE_RATE = 16000
AUDIO_MODEL_WEIGHTS = "models/weights/rawnet2_spoof.pth"
AUDIO_FAKE_THRESHOLD = 0.6
MAX_AUDIO_DURATION = 5  # seconds (edge constraint)
