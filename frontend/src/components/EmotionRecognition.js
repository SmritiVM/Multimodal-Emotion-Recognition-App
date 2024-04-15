import React, { useState, useEffect } from 'react';
import Webcam from "react-webcam";

const EmotionRecognition = () => {
  const webcamRef = React.useRef(null);

  const captureFrameAndProcess = async () => {
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
  };

  useEffect(() => {
    // Capture frame and process every 1 second (1000 milliseconds)
    const intervalId = setInterval(captureFrameAndProcess, 1000);

    // Cleanup function to clear the interval when the component unmounts
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        className='camera'
      />
    </div>
  );
};

export default EmotionRecognition;
