from utils.video_utils import extract_face_frames


class VideoPipeline:
    """
    Handles visual evidence extraction from video input.
    Gracefully degrades when no faces are detected.
    """

    def __init__(self):
        pass

    def process(self, video_path):
        """
        Returns a list of face crops ready for AI inference.
        If no faces are detected, returns an empty list instead of crashing.
        """

        faces = extract_face_frames(video_path)

        if len(faces) == 0:
            print("[VideoPipeline] WARNING: No faces detected in video.")
            return []

        return faces