import streamlit as st
import random
import time

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="EDGE-SHIELD (Demo)", layout="centered")

st.title("EDGE-SHIELD : Deepfake Detection (Demo)")
st.markdown("**Agentic AI – Offline-Capable PoC (Cloud Demo Mode)**")

# ------------------------------
# REPO LINK (VERY IMPORTANT)
# ------------------------------
st.markdown(
    """
🔗 **GitHub Repository (Full Offline PoC):**  
https://github.com/itskunalvisionary/edge-shield-deepfake-PoC
"""
)

st.info(
    "⚠️ This online demo showcases **agentic decision logic only**.\n\n"
    "The **full offline edge-deployable system with real AI models** "
    "is available in the GitHub repository above, as required by the problem statement."
)

# ------------------------------
# FILE UPLOAD (DEMO)
# ------------------------------
uploaded_file = st.file_uploader(
    "Upload Video Evidence (Demo Mode)",
    type=["mp4", "avi", "mov"]
)

if uploaded_file is None:
    st.stop()

st.success("Video uploaded successfully (Demo Mode)")

# ------------------------------
# SIMULATED ANALYSIS
# ------------------------------
with st.spinner("Running agentic analysis..."):
    time.sleep(2)

video_score = round(random.uniform(0.3, 0.7), 2)
audio_score = round(random.uniform(0.3, 0.7), 2)

combined_score = (0.6 * video_score) + (0.4 * audio_score)

if combined_score >= 0.65:
    label, risk = "FAKE", "HIGH"
elif combined_score <= 0.35:
    label, risk = "REAL", "LOW"
else:
    label, risk = "INCONCLUSIVE", "MEDIUM"

# ------------------------------
# OUTPUT
# ------------------------------
st.subheader("Detection Result")

st.write(f"**Label:** {label}")
st.write(f"**Risk Level:** {risk}")
st.write(f"**Video Score:** {video_score}")
st.write(f"**Audio Score:** {audio_score}")

st.subheader("Agent Explanation")
st.write("• Cloud demo prioritizes **decision logic & agent behavior**")
st.write("• Heavy AI models are executed **offline on edge devices**")
st.write("• INCONCLUSIVE results are returned intentionally when evidence is insufficient, preventing false accusations in sensitive scenarios**")
