from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import cv2
import numpy as np
import tensorflow as tf
import base64

# Load the Keras model
model_path = 'mask_recog.h5'
model = tf.keras.models.load_model(model_path)

# Define the classes
class_labels = ['Mask', 'No Mask']

app = Flask(__name__)
CORS(app)

def predict_mask(frame):
    # Converting frame from base64 string to numpy array
    frame_bytes = base64.b64decode(frame.split(',')[1])
    nparr = np.frombuffer(frame_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Preprocess the input frame (resize, normalize, etc.) as needed
    resized_frame = cv2.resize(frame, (224, 224))
    preprocessed_frame = resized_frame / 255.0  # Normalize pixel values to [0, 1]

    # Perform inference using the loaded Keras model
    predictions = model.predict(np.expand_dims(preprocessed_frame, axis=0))
    class_index = np.argmax(predictions)
    confidence = predictions[0][class_index]

    threshold = 0.8  # You can adjust this threshold as needed
    if confidence > threshold:
        label = class_labels[class_index]
    else:
        label = 'Unknown'

    return label

@app.route('/check-mask', methods=['POST'])
@cross_origin()
def check_mask():
    try:
        frame_data = request.json['frame']
        mask_status = predict_mask(frame_data)
        print("Mask status: ", mask_status)
        return jsonify({'mask_status': mask_status})
    except Exception as e:
        print("Error predicting mask:", str(e))
        return jsonify({'error': str(e)}) 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
