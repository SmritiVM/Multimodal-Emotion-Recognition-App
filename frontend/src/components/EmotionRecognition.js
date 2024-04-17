import React, { useState, useEffect } from 'react';
import Webcam from "react-webcam";

const EmotionRecognition = () => {
  const webcamRef = React.useRef(null);

  const captureFrameAndProcess = async () => {
    const frame = webcamRef.current.getScreenshot();

    const maskResponse = await fetch('http://localhost:5002/check-mask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ frame })
    });

    const maskData = await maskResponse.json();
    console.log("Mask Status:", maskData.mask_status);

    // Only process emotions if mask status is "No Mask"
    if (maskData.mask_status === 'No Mask') {
      const emotionResponse = await fetch('http://localhost:5000/predict_emotion', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ frame })
      });

      const emotionData = await emotionResponse.json();
      console.log("Predicted Emotion:", emotionData.emotion);
    }
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
