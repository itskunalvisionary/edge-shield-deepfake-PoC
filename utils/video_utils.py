import cv2
import numpy as np
from config.settings import (
    VIDEO_FRAME_SIZE,
    FRAME_SAMPLE_RATE,
    FACE_CASCADE_PATH,
    MIN_FACE_SIZE
)

# Load Haar Cascade once (important for performance)
face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)


def extract_face_frames(video_path):
    """
    Extracts sampled face crops from a video file.

    Returns:
        List[np.ndarray]: List of face images (RGB, resized)
    """

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise RuntimeError("Failed to open video file")

    face_frames = []
    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Power-aware sampling
        if frame_index % FRAME_SAMPLE_RATE != 0:
            frame_index += 1
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5
        )

        for (x, y, w, h) in faces:
            if w < MIN_FACE_SIZE or h < MIN_FACE_SIZE:
                continue

            face = frame[y:y+h, x:x+w]
            face = cv2.resize(face, (VIDEO_FRAME_SIZE, VIDEO_FRAME_SIZE))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

            face_frames.append(face)

        frame_index += 1

    cap.release()
    return face_frames
