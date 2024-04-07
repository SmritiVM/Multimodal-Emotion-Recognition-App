// import React, { useEffect, useRef } from 'react';
// // import * as cv from "opencv.js"; 

// function EmotionRecognition() {
//   const videoRef = useRef();
  
//   useEffect(() => {
//     // OpenCV initialization
//     cv['onRuntimeInitialized'] = () => {
//       startEmotionRecognition();
//     };
//   }, []);

//   const startEmotionRecognition = async () => {
//     // Initialize webcam
//     const videoElement = videoRef.current;
//     const constraints = { video: true };
//     const stream = await navigator.mediaDevices.getUserMedia(constraints);
//     videoElement.srcObject = stream;
    
//     // Load model
//     const classifier = await cv.imread('model.h5');
//     const emotionLabels = ['Angry', '', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise'];
    
//     // Start processing frames
//     const processFrames = () => {
//       const frame = new cv.Mat(videoElement.height, videoElement.width, cv.CV_8UC4);
//       const cap = new cv.VideoCapture(videoElement);
      
//       const detectAndDisplay = () => {
//         cap.read(frame);
//         const grayFrame = new cv.Mat();
//         cv.cvtColor(frame, grayFrame, cv.COLOR_RGBA2GRAY);
//         cv.equalizeHist(grayFrame, grayFrame);
        
//         const faces = new cv.RectVector();
//         const faceCascade = new cv.CascadeClassifier();
//         faceCascade.load('haarcascade_frontalface_alt.xml');
//         faceCascade.detectMultiScale(grayFrame, faces);
        
//         for (let i = 0; i < faces.size(); ++i) {
//           const face = faces.get(i);
//           const { x, y, width, height } = face;
//           cv.rectangle(frame, { x, y }, { x: x + width, y: y + height }, [0, 255, 0, 255], 2);
          
//           const roiGray = grayFrame.roi(face);
//           const roiResized = new cv.Mat();
//           cv.resize(roiGray, roiResized, new cv.Size(48, 48), 0, 0, cv.INTER_AREA);
          
//           // Process ROI for emotion detection
//           // You can call detectAndDisplay() here to show detected emotions on the frame
          
//           roiGray.delete();
//           roiResized.delete();
//         }
        
//         cv.imshow('canvasOutput', frame);
//         frame.delete();
//         grayFrame.delete();
//         faceCascade.delete();
//         faces.delete();
//         requestAnimationFrame(detectAndDisplay);
//       };
      
//       detectAndDisplay();
//     };
    
//     processFrames();
//   };

//   return (
//     <div>
//       <h1>Facial Emotion Recognition</h1>
//       <video ref={videoRef} autoPlay />
//       <canvas id="canvasOutput" />
//     </div>
//   );
// };

// export default EmotionRecognition;
