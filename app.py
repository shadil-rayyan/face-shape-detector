import cv2
import numpy as np

# Load the pre-trained Haar cascade classifier for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Function to detect faces, draw bounding boxes, and analyze shape
def detect_and_analyze_face(frame):
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale for efficiency

  # Detect faces using the classifier
  faces = face_cascade.detectMultiScale(gray, 1.1, 4)
  
  # Loop through detected faces
  for (x, y, w, h) in faces:
    # Draw a green bounding box around the face
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Analyze face shape (use both aspect ratio and landmarks for improved accuracy)
    face_shape = analyze_face_shape(aspect_ratio=float(w) / h, facial_landmarks=None)

    # Display face shape text on top of the bounding box
    cv2.putText(frame, f"Face Shape: {face_shape}", (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 2)

  # Display the frame with bounding boxes and shape analysis
  cv2.imshow('Face Detection with Shape Analysis', frame)

# Function to analyze face shape using aspect ratio and optional landmarks
def analyze_face_shape(aspect_ratio, facial_landmarks=None):
  if facial_landmarks is not None:
    # Implement landmark-based analysis here (more accurate)

    # Example logic for Triangle and Heart shapes (replace with more comprehensive analysis)
    # This is a simplified version and might require further refinement for better accuracy.

    # Calculate brow line length, jawline length, forehead width, and chin width
    brow_length = np.linalg.norm(facial_landmarks[17] - facial_landmarks[26])
    jawline_length = np.linalg.norm(facial_landmarks[48] - facial_landmarks[54])
    forehead_width = np.linalg.norm(facial_landmarks[17] - facial_landmarks[21])
    chin_width = np.linalg.norm(facial_landmarks[8] - facial_landmarks[9])

    # Triangle: consider both aspect ratio and brow-to-jaw ratio
    if aspect_ratio > 1.0 and brow_length / jawline_length > 1.2:
      face_shape = "Triangle"

    # Heart: consider aspect ratio, chin width, and forehead width
    elif aspect_ratio > 1.1 and chin_width < forehead_width / 2:
      face_shape = "Heart"

    # If none of the above conditions are met, consider other shapes or refer to more advanced landmark analysis techniques
    else:
      # ... (consider other shapes or improve landmark analysis)
      face_shape = "Unknown"  # Placeholder for unclassified shapes using landmarks

    return face_shape

  else:  # Fallback to aspect ratio-based classification
    # Enhanced shape classification using aspect ratio and additional conditions:
    face_shape = "Unknown"
    if aspect_ratio > 1.3:
      face_shape = "Oval"
    elif aspect_ratio < 0.85:
      face_shape = "Round"
    elif aspect_ratio > 1.1:
      face_shape = "Square/Rectangular"
    else:
      if abs(aspect_ratio - 1.0) < 0.1:
        face_shape = "Diamond"
      else:
        face_shape = "Unknown"  # Handle cases that don't fit any of the above categories

    return face_shape

# Capture video from webcam (or provide a video file path)
cap = cv2.VideoCapture(0)  # Change to video file path if desired

while True:
  # Capture frame-by-frame
  ret, frame = cap.read()
  
  # Check if frame capture is successful
  if not ret:
    print("Failed to capture frame!")
    break

  # Detect and analyze faces in the frame
  detect_and_analyze_face(frame)

  # Press 'q' to quit
  if cv2.waitKey(1) == ord('q'):
    break

# Release capture resources
cap.release()
cv2.destroyAllWindows()
