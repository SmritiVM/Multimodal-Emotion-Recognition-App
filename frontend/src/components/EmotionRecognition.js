import React, { useState, useEffect } from 'react';
import Webcam from "react-webcam";

const EmotionRecognition = () => {
  const [processedFrame, setProcessedFrame] = useState('');
  const webcamRef = React.useRef(null);

  const captureFramesAndProcess = async () => {
    const frame = webcamRef.current.getScreenshot();

    const response = await fetch('http://localhost:5000/process_frame', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ frame })
    });

    const data = await response.json();
    // console.log("Processed Frame Data:", data.processed_frame); // Log processed frame data for debugging
    setProcessedFrame(data.processed_frame);

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
      {processedFrame && <img src={processedFrame} alt="Processed Frame" />}
    </div>
  );
};

export default EmotionRecognition;
