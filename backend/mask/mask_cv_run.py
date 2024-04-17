import cv2
import numpy as np
from flask import Flask, render_template, Response
import tensorflow as tf

# Load the Keras model
model_path = 'mask_recog.h5'
model = tf.keras.models.load_model(model_path)

# Define the classes
class_labels = ['Mask', 'No Mask']

app = Flask(__name__)

def predict_mask(frame):
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

def video_feed():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        label = predict_mask(frame)

        # Display the prediction
        cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Encode the frame as JPEG
        _, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed_route():
    return Response(video_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)


# import cv2
# import numpy as np
# import tensorflow as tf

# # Load the Keras model
# model_path = 'mask_recog.h5'
# model = tf.keras.models.load_model(model_path)

# # Initialize the video stream
# cap = cv2.VideoCapture(0)  # Use 0 for webcam, or provide the path to your video file

# # Define the classes
# class_labels = ['Mask', 'No Mask']

# # Loop over frames from the video stream
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Preprocess the input frame (resize, normalize, etc.) as needed
#     resized_frame = cv2.resize(frame, (224, 224))
#     preprocessed_frame = resized_frame / 255.0  # Normalize pixel values to [0, 1]

#     # Perform inference using the loaded Keras model
#     predictions = model.predict(np.expand_dims(preprocessed_frame, axis=0))
#     class_index = np.argmax(predictions)
#     label = class_labels[class_index]
#     confidence = predictions[0][class_index]

#     threshold = 0.8  # You can adjust this threshold as needed
#     if confidence > threshold:
#         label = class_labels[class_index]
#     else:
#         label = 'Unknown'

#     # Display the prediction
#     cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
#     # Display the output frame
#     cv2.imshow("Frame", frame)

#     # Break the loop if 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the video capture object and close all windows
# cap.release()
# cv2.destroyAllWindows()
