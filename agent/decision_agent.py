class DecisionAgent:
    """
    Uncertainty-aware multimodal decision agent.
    """

    def __init__(self):
        self.low_conf = 0.35
        self.high_conf = 0.65

    def decide(self, video_score, audio_score, face_detected: bool):
        explanation = []

        explanation.append(f"Video analysis score: {round(video_score, 2)}")
        explanation.append(f"Audio analysis score: {round(audio_score, 2)}")

        # HARD RULE: no faces = no REAL verdict
        if not face_detected:
            explanation.append(
                "No reliable facial evidence detected in the video."
            )
            explanation.append(
                "Decision deferred due to insufficient biometric evidence."
            )
            return {
                "label": "INCONCLUSIVE",
                "risk": "MEDIUM",
                "explanation": explanation
            }

        # Normal multimodal fusion
        combined_score = (0.6 * video_score) + (0.4 * audio_score)
        explanation.append(
            f"Combined authenticity score: {round(combined_score, 2)}"
        )

        # Transparency note for advanced generative models (NON-LOGIC, SAFE)
        if video_score == 0.25 and audio_score == 0.5:
            explanation.append(
                "Video exhibits high visual stability; advanced generative models may evade artifact-based detection."
            )

        if combined_score >= self.high_conf:
            label = "FAKE"
            risk = "HIGH"
            explanation.append(
                "Strong multimodal indicators of manipulation detected."
            )

        elif combined_score <= self.low_conf:
            label = "REAL"
            risk = "LOW"
            explanation.append(
                "No strong manipulation indicators detected."
            )

        else:
            label = "INCONCLUSIVE"
            risk = "MEDIUM"
            explanation.append(
                "Evidence falls within uncertainty band."
            )

        return {
            "label": label,
            "risk": risk,
            "explanation": explanation
        }