import React, { useState, useEffect } from 'react';
import Webcam from "react-webcam";

const EmotionRecognition = () => {
  const webcamRef = React.useRef(null);

  const captureFramesAndProcess = async () => {
    const frame = webcamRef.current.getScreenshot();

    const response = await fetch('http://localhost:5000/predict_emotion', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ frame })
    });

    const data = await response.json();
    console.log("Predicted Emotion:", data.emotion);

    requestAnimationFrame(captureFramesAndProcess);
  };

  useEffect(() => {
    captureFramesAndProcess();
  }, []);

  return (
    <div>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
      />
    </div>
  );
};

export default EmotionRecognition;
