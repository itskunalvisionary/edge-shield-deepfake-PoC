import streamlit as st
import os
import time

# ------------------------------
# Streamlit UI (LIGHTWEIGHT ONLY)
# ------------------------------

st.set_page_config(page_title="EDGE-SHIELD", layout="centered")

st.title("EDGE-SHIELD : Deepfake Detection PoC")
st.markdown("**Offline Agentic AI System for Video + Audio Authenticity**")

st.divider()

st.subheader("Step 1: Upload Video Evidence")
st.write(
    "Upload a video file to analyze both **facial** and **voice authenticity** "
    "using an offline, agentic AI pipeline."
)

uploaded_file = st.file_uploader(
    "Supported formats: MP4, AVI, MOV",
    type=["mp4", "avi", "mov"]
)

if uploaded_file is None:
    st.info("Please upload a video file to begin analysis.")

# =====================================================
# HEAVY IMPORTS + MODELS (ONLY AFTER FILE IS UPLOADED)
# =====================================================

if uploaded_file is not None:

    # ---------- Heavy imports ----------
    from pipelines.video_pipeline import VideoPipeline
    from pipelines.audio_pipeline import AudioPipeline
    from agent.decision_agent import DecisionAgent
    from utils.logger import log_event

    # ---------- Save uploaded video ----------
    os.makedirs("outputs/temp", exist_ok=True)
    temp_video_path = "outputs/temp/input_video.mp4"

    with open(temp_video_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("Video uploaded successfully.")

    # ===============================
    # VIDEO ANALYSIS (REAL MODEL)
    # ===============================

    video_progress = st.progress(0, text="Initializing video analysis...")
    video_start = time.time()

    video_pipeline = VideoPipeline()
    video_progress.progress(25, "Extracting face frames...")
    try:
        faces = video_pipeline.process(temp_video_path)
    except Exception as e:
        print("[App] Video pipeline failed:", e)
        faces = []

    st.write(
    f"Frames analyzed: {len(faces)} | "
    f"Faces detected in {len(faces)} frames"
    )

    from models.video_model import VideoDeepfakeModel

    video_progress.progress(60, "Running video deepfake model...")
    video_detector = VideoDeepfakeModel()  # ✅ Xception-based real model
    video_score = video_detector.predict(faces)

    video_progress.progress(100, "Video analysis complete")
    video_time = round(time.time() - video_start, 2)

    # ===============================
    # AUDIO ANALYSIS (RAWNET2LITE)
    # ===============================

    audio_progress = st.progress(0, text="Initializing audio analysis...")
    audio_start = time.time()

    audio_progress.progress(30, "Extracting audio signal...")
    audio_pipeline = AudioPipeline()  # ✅ RawNet2Lite (NO DUMMY)

    audio_progress.progress(70, "Running audio spoof detection...")
    audio_score = audio_pipeline.process(temp_video_path)

    audio_progress.progress(100, "Audio analysis complete")
    audio_time = round(time.time() - audio_start, 2)

    # ===============================
    # AGENT DECISION
    # ===============================

    agent = DecisionAgent()
    decision = agent.decide(
        video_score=video_score,
        audio_score=audio_score,
        face_detected=len(faces) > 0
    )

    # ===============================
    # FORENSIC LOGGING
    # ===============================

    log_event({
        "video_score": round(video_score, 3),
        "audio_score": round(audio_score, 3),
        "label": decision["label"],
        "risk": decision["risk"],
        "video_time_sec": video_time,
        "audio_time_sec": audio_time
    })

    # ===============================
    # OUTPUT
    # ===============================

    st.subheader("Detection Result")

    st.write(f"**Label:** {decision['label']}")
    st.write(f"**Risk Level:** {decision['risk']}")
    st.write(f"**Video Fake Probability:** {round(video_score, 2)}")
    st.write(f"**Audio Fake Probability:** {round(audio_score, 2)}")

    st.subheader("Performance Metrics")
    st.write(f"Video Analysis Time: **{video_time} sec**")
    st.write(f"Audio Analysis Time: **{audio_time} sec**")

    st.subheader("Agent Explanation")
    for line in decision["explanation"]:
        st.write("•", line)

    st.write("• This system detects manipulation artifacts, not intent or authenticity.")
    st.write("• High-fidelity generative models may evade artifact-based detectors.")
    st.write("• Uncertainty is surfaced to avoid false accusations.")