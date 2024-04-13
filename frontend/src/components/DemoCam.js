import React, { useRef, useEffect } from 'react';
import * as tf from "@tensorflow/tfjs";
import * as facemesh from "@tensorflow-models/facemesh";
import Webcam from "react-webcam";
import { drawMesh } from './utilities';

export default function DemoCam() {
  // Setup references
  const webcamRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    runFacemesh();
  }, []);

  // Load facemesh
  const runFacemesh = async () => {
    const net = await facemesh.load({
      inputResolution: { width: 640, height: 480 },
      scale: 0.8
    });

    setInterval(() => {
      detect(net);
    }, 100);
  };

  // Detect function
const detect = async (net) => {
  if (
    typeof webcamRef.current !== "undefined" &&
    webcamRef.current !== null &&
    webcamRef.current.video.readyState === 4
  ) {
    // Get video properties
    const video = webcamRef.current.video;
    const videoWidth = video.videoWidth;
    const videoHeight = video.videoHeight;

    // Set video width and height
    video.width = videoWidth;
    video.height = videoHeight;

    // Set canvas width and height
    canvasRef.current.width = videoWidth;
    canvasRef.current.height = videoHeight;

    // Make detections
    const faces = await net.estimateFaces(video);

    if (faces.length > 0) {
      // Get canvas context for drawing
      const ctx = canvasRef.current.getContext("2d");

      // Clear previous drawings
      ctx.clearRect(0, 0, videoWidth, videoHeight);

      // Draw bounding boxes and keypoints
      drawMesh(faces, ctx);

      // Preprocess and predict emotions for each detected face
      const predictions = await Promise.all(faces.map(async (face) => {
        const tensor = preprocessImage(video, face);
        if (tensor) {
          return predictEmotions(tensor);
        } else {
          return null;
        }
      }));

      console.log(predictions); // Log all the predictions
    }
  }
};


    // Preprocess the image
    const preprocessImage = (video, face) => {
    console.log("Face:", face);
    if (!face || !face.boundingBox || !face.boundingBox.topLeft || !face.boundingBox.bottomRight) {
      console.error("Invalid face or bounding box:", face);
      return null;
    }

    const x = face.boundingBox.topLeft[0];
    const y = face.boundingBox.topLeft[1];
    const width = face.boundingBox.bottomRight[0] - x;
    const height = face.boundingBox.bottomRight[1] - y;

    if (!isFinite(x) || !isFinite(y) || !isFinite(width) || !isFinite(height)) {
      console.error("Invalid bounding box dimensions:", x, y, width, height);
      return null;
    }

    console.log("Bounding Box:", { x, y, width, height });

    


    const imageData = canvasRef.current.getContext("2d").getImageData(x, y, width, height);

    console.log("Image Data:", imageData);

    const tensor = tf.browser.fromPixels(imageData)
      .resizeNearestNeighbor([48, 48])
      .toFloat()
      .div(tf.scalar(255.0))
      .expandDims();

    return tensor;
  };




  // Run the emotion recognition model
  const predictEmotions = async (tensor) => {
    const response = await fetch('http://localhost:3000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ input: tensor.arraySync() })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log('Predictions:', data.predictions);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }    

  return (
    <div>
      <Webcam
        ref={webcamRef}
        style={{
          position: "absolute",
          marginLeft: "auto",
          marginRight: "auto",
          left: 0,
          right: 0,
          textAlign: "center",
          zIndex: 9,
          width: 640,
          height: 480
        }}
      />
      <canvas
        ref={canvasRef}
        style={{
          position: "absolute",
          marginLeft: "auto",
          marginRight: "auto",
          left: 0,
          right: 0,
          textAlign: "center",
          zIndex: 9,
          width: 640,
          height: 480
        }}
      />
    </div>
  );
}
