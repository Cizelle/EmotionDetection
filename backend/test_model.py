# backend/test_model.py
from transformers import pipeline
import traceback
import os

MODEL_NAME = "Dpngtm/wav2vec2-emotion-recognition"
emotion_pipeline = None

# Manually create the label mapping
HUMAN_READABLE_LABELS = {
    'LABEL_0': 'neutral',
    'LABEL_1': 'calm',
    'LABEL_2': 'happy',
    'LABEL_3': 'sad',
    'LABEL_4': 'angry',
    'LABEL_5': 'fearful',
    'LABEL_6': 'disgust',
    'LABEL_7': 'surprised',
}

try:
    emotion_pipeline = pipeline("audio-classification", model=MODEL_NAME, device=-1)
    print("✅ Loaded audio-emotion model:", MODEL_NAME)

    # Note: The model's raw labels are not human-readable
    print("👉 Raw labels:", emotion_pipeline.model.config.id2label)

except Exception as e:
    print("❌ Error loading model:", e)
    traceback.print_exc()
    emotion_pipeline = None

def predict_emotion(audio_path: str):
    if emotion_pipeline is None:
        return "Model not loaded"
    if not os.path.exists(audio_path):
        return "No audio file"

    try:
        results = emotion_pipeline(audio_path)
        if not results:
            return "No prediction"

        top = max(results, key=lambda x: x.get("score", 0))
        raw_label = top.get("label", "unknown")
        
        # Get the human-readable label from our manual mapping
        human_readable_label = HUMAN_READABLE_LABELS.get(raw_label, "unknown")
        
        return human_readable_label

    except Exception as e:
        print("❌ Error predicting emotion:")
        traceback.print_exc()
        return "Prediction failed"