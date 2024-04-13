from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import cv2
import numpy as np
from keras.models import load_model
from tensorflow.keras.preprocessing import image
import base64

app = Flask(__name__)
CORS(app)  # Enabling CORS(cross-origin resource sharing) for all routes

# Loading the face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Loading the emotion recognition model
classifier = load_model("model.h5")
emotion_labels = ['Angry', '', 'Fear', 'Happy','Neutral', 'Sad', 'Surprise']


def process_frame(frame):
    # Converting frame from base64 string to numpy array
    frame_bytes = base64.b64decode(frame.split(',')[1])
    nparr = np.frombuffer(frame_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Converting frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.equalizeHist(gray_frame) # Performing histogram equalization
    
    # Detecting faces
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
            return label
    
    # If no face is detected
    return None

# Defining a route to receive video frames and predict emotion
@app.route('/predict_emotion', methods=['POST'])
@cross_origin()  # Enable CORS for this route
def predict_emotion():
    try:
        frame_data = request.json['frame']
        # print("Received frame data:", frame_data)  
        emotion = process_frame(frame_data)
        print("Predicted emotion:", emotion)  
        return jsonify({'emotion': emotion})
    except Exception as e:
        print("Error predicting emotion:", str(e))
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
