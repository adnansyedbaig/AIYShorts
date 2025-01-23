import cv2
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips
from Components.Speaker import detect_faces_and_speakers, Frames

def crop_to_vertical(input_video_path, output_video_path):
    detect_faces_and_speakers(input_video_path, "DecOut.mp4")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(input_video_path, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    vertical_height = original_height
    vertical_width = int(vertical_height * 9 / 16)  # 16:9 aspect ratio

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (vertical_width, vertical_height))

    for _ in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            center_x = x + w // 2
            start_x = max(0, center_x - vertical_width // 2)
            end_x = min(original_width, center_x + vertical_width // 2)
            cropped_frame = frame[:, start_x:end_x]
        else:
            cropped_frame = frame[:, :vertical_width]

        out.write(cropped_frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def combine_videos(video1_path, video2_path, output_path):
    clip1 = VideoFileClip(video1_path)
    clip2 = VideoFileClip(video2_path)
    final_clip = concatenate_videoclips([clip1, clip2])
    final_clip.write_videofile(output_path)
