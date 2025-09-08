# backend/test_model.py
from transformers import pipeline

# Load Hugging Face pipeline once at startup
try:
    emotion_pipeline = pipeline(
        "audio-classification",
        model="superb/wav2vec2-base-superb-er"
    )
    print("✅ Hugging Face model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    emotion_pipeline = None


def predict_emotion(audio_path: str):
    """
    Predict emotion using Hugging Face wav2vec2 model.
    """
    if emotion_pipeline is None:
        return "Model not loaded"

    try:
        results = emotion_pipeline(audio_path)

        # Pick top emotion by score
        best = max(results, key=lambda x: x["score"])
        return best["label"]

    except Exception as e:
        print(f"❌ Error predicting emotion: {e}")
        return "Prediction failed"
