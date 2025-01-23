import cv2
import numpy as np
import webrtcvad
import wave
import contextlib
from pydub import AudioSegment
import os

# Update paths to the model files
prototxt_path = "models/deploy.prototxt"
model_path = "models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
temp_audio_path = "temp_audio.wav"

# Load DNN model
net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

# Initialize VAD
vad = webrtcvad.Vad(2)  # Aggressiveness mode from 0 to 3

def voice_activity_detection(audio_frame, sample_rate=16000):
    return vad.is_speech(audio_frame, sample_rate)

def extract_audio_from_video(video_path, output_audio_path):
    video = AudioSegment.from_file(video_path)
    video.export(output_audio_path, format="wav")

def detect_faces_in_frame(frame):
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    faces = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
            (startX, startY, endX, endY) = box.astype("int")
            faces.append((startX, startY, endX, endY))
    return faces

def detect_faces_and_speakers(video_file, output_file):
    extract_audio_from_video(video_file, temp_audio_path)

    with contextlib.closing(wave.open(temp_audio_path, 'rb')) as wf:
        sample_rate = wf.getframerate()
        frames = wf.readframes(wf.getnframes())
        audio_frame = np.frombuffer(frames, dtype=np.int16)

    is_speech = voice_activity_detection(audio_frame, sample_rate)
    print(f"Voice activity detected: {is_speech}")

    cap = cv2.VideoCapture(video_file)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, cap.get(cv2.CAP_PROP_FPS), (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        faces = detect_faces_in_frame(frame)
        for (startX, startY, endX, endY) in faces:
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

        out.write(frame)

    cap.release()
    out.release()
    print(f"Processed video saved to {output_file}")

Frames = []  # Placeholder for frames data

if __name__ == "__main__":
    video_path = "input_video.mp4"
    output_path = "output_video.mp4"
    detect_faces_and_speakers(video_path, output_path)
