# EDGE-SHIELD

**Offline Deepfake Detection – Proof of Concept**

---

## Overview

EDGE-SHIELD is an offline artificial intelligence system designed to analyze videos and determine whether they are authentic, manipulated, or require further investigation. The system operates independently on edge devices such as laptops, field computers, and body-worn cameras, making it suitable for environments where internet connectivity is limited or unavailable.

This project represents a proof of concept demonstration and is not intended as a final commercial product.

---

## Problem Statement

Manipulated video content poses significant challenges in modern digital environments:

- Misinformation can spread rapidly through fabricated media
- False evidence may be created to misrepresent events or individuals
- Public trust in digital content continues to erode

However, incorrectly labeling genuine content as manipulated can cause serious harm. EDGE-SHIELD addresses this concern by prioritizing accuracy and avoiding premature conclusions when evidence is insufficient.

---

## System Architecture

EDGE-SHIELD employs a multi-stage verification process:

1. Users submit video files through the interface
2. The system conducts two parallel analyses:
   - Visual analysis examining facial consistency across frames
   - Audio analysis detecting synthetic voice patterns
3. A decision agent evaluates both analysis results
4. The system returns one of three classifications:
   - REAL
   - FAKE
   - INCONCLUSIVE

---

## Visual Analysis Module

The visual analysis component performs the following operations:

- Extracts individual frames containing faces from the uploaded video
- Applies a deep learning model based on the Xception architecture
- Evaluates consistency patterns across multiple frames

Rather than relying on single-frame assessment, the system examines temporal stability and identifies abrupt visual anomalies. This approach addresses the challenge that modern synthetic videos often appear convincing when viewed frame by frame.

---

## Audio Analysis Module

The audio verification system operates through these steps:

- Extracts the audio track from the video file
- Segments the audio into manageable portions for analysis
- Applies a compact detection model inspired by RawNet architecture

The module identifies characteristics commonly associated with synthetic audio, including artificially uniform vocal patterns and unnatural signal stability.

---

## Decision Agent

EDGE-SHIELD incorporates an intelligent decision agent rather than fixed classification rules.

The agent operates according to these principles:

- Assigns greater weight to visual evidence compared to audio indicators
- Declines to classify content as authentic when facial data is absent
- Avoids making determinations based on insufficient evidence

Classification decisions rely on confidence thresholds rather than arbitrary assumptions.

---

## The Importance of Inconclusive Results

When the system cannot confidently classify content, it returns an INCONCLUSIVE verdict. This outcome is deliberate and represents responsible system design.

Rationale for inconclusive classifications:

- Advanced generative models produce increasingly sophisticated content with minimal detectable artifacts
- Some manipulated content lacks clear indicators of fabrication
- Incorrectly labeling ambiguous content carries significant risks

An INCONCLUSIVE result indicates that current evidence does not support safe classification. This approach reflects responsible artificial intelligence development principles rather than a system limitation.

---

## Real-World Applications

EDGE-SHIELD offers several practical advantages:

- Functions without internet connectivity
- Operates independently of cloud services
- Runs efficiently on standard CPU hardware
- Provides transparent reasoning for classifications
- Minimizes false accusations through conservative decision-making
- Designed for deployment on edge computing devices

These characteristics make the system appropriate for:

- Law enforcement demonstrations and evaluations
- Field investigation scenarios
- Security research applications
- Policy assessment and development

---

## Project Organization

```
agent/        Decision logic and classification rules
models/       Neural network architectures
pipelines/    Video and audio processing workflows
config/       Configuration parameters and thresholds
outputs/      Analysis logs and temporary files
app.py        Streamlit web interface
```

---

## Installation and Usage

Install required dependencies:

```bash
pip install -r requirements.txt
```

Launch the application:

```bash
streamlit run app.py
```

Access the interface through your web browser and upload a video file for analysis.

---

## Design Philosophy

This proof of concept prioritizes three core principles:

- **Trustworthiness**: Classifications are based on verifiable evidence
- **Transparency**: The system provides clear explanations for its conclusions
- **Risk Awareness**: Conservative decision-making prevents harmful misclassifications

In sensitive applications, withholding judgment when evidence is insufficient often represents the most responsible course of action. EDGE-SHIELD demonstrates this philosophy through its design and implementation.

---

## Author

Kunal Pandit
