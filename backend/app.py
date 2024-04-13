from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import cv2
import numpy as np
from keras.models import load_model
from tensorflow.keras.preprocessing import image
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the emotion recognition model
classifier = load_model("model.h5")
emotion_labels = ['Angry', '', 'Fear', 'Happy','Neutral', 'Sad', 'Surprise']

# Define a function to process each frame
def process_frame(frame):
    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.equalizeHist(gray_frame)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray_frame)
    
    for (x, y, w, h) in faces:
        roi_gray = gray_frame[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
        
        if np.sum([roi_gray]) != 0:
            roi = roi_gray.astype('float') / 255.0
            roi = image.img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            
            # Predict emotion
            prediction = classifier.predict(roi)[0]
            label = emotion_labels[prediction.argmax()]
            cv2.putText(frame, label, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    
    return frame

# Define a route to receive video frames
@app.route('/process_frame', methods=['POST'])
@cross_origin()  # Enable CORS for this route
def process_frame_route():
    # Convert frame from base64 string to numpy array
    frame_data = request.json['frame']
    frame_bytes = base64.b64decode(frame_data.split(',')[1])
    nparr = np.frombuffer(frame_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Process frame
    processed_frame = process_frame(frame)
    
    # Convert processed frame to base64 string
    _, encoded_frame = cv2.imencode('.jpg', processed_frame)
    processed_frame_data = 'data:image/jpeg;base64,' + base64.b64encode(encoded_frame).decode()
    
    return jsonify({'processed_frame': processed_frame_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
