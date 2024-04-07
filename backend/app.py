from flask import Flask, request, jsonify
import cv2 as cv
import numpy as np
from keras.models import load_model
from tensorflow.keras.utils import img_to_array
from keras.preprocessing import image

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'

app = Flask(__name__)

# Load the face cascade
face_cascade_name = "haarcascade_frontalface_alt.xml"
face_cascade = cv.CascadeClassifier(cv.samples.findFile(face_cascade_name))

# Load the emotion detection model
classifier = load_model("model.h5")
emotion_labels = ['Angry', '', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

def detect_emotion(frame):
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray_frame = cv.equalizeHist(gray_frame)
    faces = face_cascade.detectMultiScale(gray_frame)

    emotions = []

    for (x,y,w,h) in faces:
        roi_gray = gray_frame[y : y + h, x : x + w]
        roi_gray = cv.resize(roi_gray, (48, 48), interpolation = cv.INTER_AREA)

        if np.sum([roi_gray]) != 0:
            roi = roi_gray.astype('float') / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            prediction = classifier.predict(roi)[0]
            label = emotion_labels[prediction.argmax()]
            emotions.append({'label': label, 'position': (x, y)})

    return emotions

@app.route('/detect_emotions', methods=['POST'])
def detect_emotions():
    image_file = request.files['image']
    nparr = np.frombuffer(image_file.read(), np.uint8)
    frame = cv.imdecode(nparr, cv.IMREAD_COLOR)
    emotions = detect_emotion(frame)
    return jsonify(emotions)

if __name__ == '__main__':
    app.run(debug=True)
