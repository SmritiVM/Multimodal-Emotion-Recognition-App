import cv2
import numpy as np
import tensorflow as tf

# Load the Keras model
model_path = 'mask_recog.h5'
model = tf.keras.models.load_model(model_path)

# Initialize the video stream
cap = cv2.VideoCapture(0)  # Use 0 for webcam, or provide the path to your video file

# Define the classes
class_labels = ['Mask', 'No Mask']

# Loop over frames from the video stream
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the input frame (resize, normalize, etc.) as needed
    resized_frame = cv2.resize(frame, (224, 224))
    preprocessed_frame = resized_frame / 255.0  # Normalize pixel values to [0, 1]

    # Perform inference using the loaded Keras model
    predictions = model.predict(np.expand_dims(preprocessed_frame, axis=0))
    class_index = np.argmax(predictions)
    label = class_labels[class_index]
    confidence = predictions[0][class_index]

    threshold = 0.8  # You can adjust this threshold as needed
    if confidence > threshold:
        label = class_labels[class_index]
    else:
        label = 'Unknown'

    # Display the prediction
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Display the output frame
    cv2.imshow("Frame", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
