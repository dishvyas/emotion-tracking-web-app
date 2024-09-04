import cv2
import numpy as np
from keras.utils import img_to_array
from keras.models import load_model


class VideoCamera(object):
    def __init__(self):
        detection_model_path = 'haarcascade_files/haarcascade_frontalface_default.xml'
        emotion_model_path = 'models/fer2013_mini_XCEPTION.107-0.66.hdf5'

        # Load Haar Cascade model
        self.face_detection = cv2.CascadeClassifier(detection_model_path)
        if self.face_detection.empty():
            raise Exception("Error loading Haar Cascade model for face detection.")

        print("Haar Cascade model loaded successfully.")

        # Load emotion detection model
        try:
            self.emotion_classifier = load_model(emotion_model_path, compile=False)
            print("Emotion detection model loaded successfully.")
        except Exception as e:
            raise Exception(f"Error loading emotion detection model: {e}")

        self.EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

        # Initialize camera
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise Exception("Could not open video source")

        print("Camera initialized successfully.")

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        if self.camera.isOpened():
            self.camera.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        ret, frame = self.camera.read()
        if not ret:
            print("Failed to grab frame")
            return None, None  # Return None for both frame and emotion

        frame = cv2.resize(frame, (300, 300))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_detection.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        emotion_label = "Neutral"  # Default emotion

        if len(faces) > 0:
            (fX, fY, fW, fH) = sorted(faces, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]), reverse=True)[0]
            roi = gray[fX:fX + fW, fY:fY + fH]
            roi = cv2.resize(roi, (64, 64))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            preds = self.emotion_classifier.predict(roi)[0]
            emotion_label = self.EMOTIONS[preds.argmax()]

            # Draw label on the frame
            cv2.putText(frame, emotion_label, (fX, fY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            cv2.rectangle(frame, (fX, fY), (fX + fW, fY + fH), (0, 0, 255), 2)

        # Encode the frame in JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes() if ret else None, emotion_label


if __name__ == "__main__":
    print("Starting the script...")

    try:
        print("Initializing camera...")
        cam = VideoCamera()
        print("Camera initialized.")
    except Exception as e:
        print(f"Exception during initialization: {e}")
    
    while True:
        frame = cam.get_frame()
        if frame is None:
            break
        # Convert bytes back to image for display
        img = cv2.imdecode(np.frombuffer(frame, np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('Emotion Detection', img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.cleanup()