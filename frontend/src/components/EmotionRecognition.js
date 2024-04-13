import React, { useState } from 'react';
import Webcam from "react-webcam";

const EmotionRecognition = () => {
  const [processedFrame, setProcessedFrame] = useState('');

  const captureFrame = async (webcamRef) => {
    const frame = webcamRef.current.getScreenshot();
    
    // Send frame to Flask server for processing
    const response = await fetch('http://localhost:5000/process_frame', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ frame })
    });
    
    const data = await response.json();
    setProcessedFrame(data.processed_frame);
  };

  const webcamRef = React.useRef(null);

  return (
    <div>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
      />
      <button onClick={() => captureFrame(webcamRef)}>Capture Frame</button>
      {processedFrame && <img src={processedFrame} alt="Processed Frame" />}
    </div>
  );
};

export default EmotionRecognition;
