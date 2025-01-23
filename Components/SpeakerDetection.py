import cv2
import numpy as np
from YoutubeDownloader import download_youtube_video

# Face Detection function
def detect_faces(video_file):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Load the video
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_file}")
        return []

    faces = []

    # Detect and store unique faces
    while len(faces) < 5:
        ret, frame = cap.read()
        if not ret:
            break  # Exit loop if no more frames are available

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detected_faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Iterate through the detected faces
        for (x, y, w, h) in detected_faces:
            face = gray[y:y+h, x:x+w]
            if not any(np.array_equal(face, existing_face) for existing_face in faces):
                faces.append(face)
                if len(faces) >= 5:
                    break

    cap.release()
    return faces

if __name__ == "__main__":
    youtube_url = input("Enter YouTube video URL: ")
    video_path = download_youtube_video(youtube_url)
    faces = detect_faces(video_path)
    print(f"Detected {len(faces)} unique faces")
