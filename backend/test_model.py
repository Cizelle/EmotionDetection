# backend/test_model.py
from transformers import pipeline
import traceback
import os

MODEL_NAME = "Dpngtm/wav2vec2-emotion-recognition"

try:
    emotion_pipeline = pipeline("audio-classification", model=MODEL_NAME, device=-1)
    print("✅ Loaded audio-emotion model:", MODEL_NAME)
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
        return top.get("label", "unknown")
    except Exception as e:
        print("❌ Error predicting emotion:")
        traceback.print_exc()
        return "Prediction failed"
