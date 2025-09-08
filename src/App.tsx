// src/App.tsx
import React, { useState } from 'react';
import { useReactMediaRecorder } from 'react-media-recorder';

const App: React.FC = () => {
    // useState with type annotation for the emotion string
    const [emotion, setEmotion] = useState<string>('');
    
    // The hook is typed automatically, so no changes needed here
    const { status, startRecording, stopRecording, mediaBlobUrl } = useReactMediaRecorder({ audio: true });

    const handleAnalyze = async () => {
        if (!mediaBlobUrl) return;

        try {
            const audioBlob = await fetch(mediaBlobUrl).then(res => res.blob());
            const formData = new FormData();
            formData.append('audio', audioBlob, 'voice_recording.wav');

            const response = await fetch('http://localhost:5000/predict', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();
            setEmotion(data.emotion);
        } catch (error) {
            console.error("Error sending audio to backend:", error);
            setEmotion('Error analyzing emotion.');
        }
    };

    return (
        <div>
            <h1>Speech Emotion Detector</h1>
            <p>Recording Status: {status}</p>
            <button onClick={startRecording}>Start Recording</button>
            <button onClick={stopRecording}>Stop Recording</button>
            {mediaBlobUrl && (
                <div>
                    <audio src={mediaBlobUrl} controls />
                    <button onClick={handleAnalyze}>Analyze Emotion</button>
                </div>
            )}
            {emotion && <h2>Detected Emotion: {emotion}</h2>}
        </div>
    );
};

export default App;