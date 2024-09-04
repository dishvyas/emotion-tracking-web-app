print("Starting the script...")
import cv2
import numpy as np
print("here")
# import tensorflow
# from tensorflow import keras
from keras.models import load_model
print("here")


# Load the pre-trained emotion detection model
print("Loading model...")
model = load_model('models/fer2013_mini_XCEPTION.107-0.66.hdf5')  # Update with the correct path
print("Model loaded.")
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
print("Emotion labels loaded.")

# Initialize the face detector (Haar Cascade)
print("Loading Haar Cascade...")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
print("Haar Cascade loaded.")

# Start video capture (webcam)
cap = cv2.VideoCapture(0)
print("Video capture started.")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    print("Frame captured.")
    
    # Convert to grayscale for the face detector
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    print(f"Detected {len(faces)} faces")

    for (x, y, w, h) in faces:
        # Extract the face region
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (64, 64))
        face = face / 255.0
        face = face.reshape(1, 64, 64, 1)  # Update to 64x64 instead of 48x48
        
        # Predict emotion
        predictions = model.predict(face)
        emotion_index = np.argmax(predictions)
        emotion_label = emotion_labels[emotion_index]
        
        # Draw a rectangle around the face and overlay the emotion label
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, emotion_label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    
    # Display the resulting frame
    cv2.imshow('Emotion Detection', frame)
    
    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()

