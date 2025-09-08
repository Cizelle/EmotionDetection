# backend/server.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import test_model  # emotion detection logic
import traceback   # <-- add this

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    audio_path = None  # initialize to avoid reference before assignment
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file found'}), 400

        audio_file = request.files['audio']

        # Save temporarily
        audio_path = "temp_recording.wav"
        audio_file.save(audio_path)

        # Debug: confirm file exists and size
        print(f"👉 Received file, saved at {audio_path}, size: {os.path.getsize(audio_path)} bytes")

        # Run prediction
        emotion = test_model.predict_emotion(audio_path)

        print(f"✅ Predicted emotion: {emotion}")
        return jsonify({'emotion': emotion})

    except Exception as e:
        print("❌ Error in /predict endpoint:")
        traceback.print_exc()  # full stack trace
        return jsonify({'error': str(e)}), 500

    finally:
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
