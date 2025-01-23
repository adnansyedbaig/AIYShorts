from moviepy.editor import VideoFileClip
import subprocess

def extractAudio(video_path):
    try:
        video_clip = VideoFileClip(video_path)
        audio_path = "audio.wav"
        video_clip.audio.write_audiofile(audio_path)
        video_clip.close()
        print(f"Extracted audio to: {audio_path}")
        return audio_path
    except Exception as e:
        print(f"An error occurred while extracting audio: {e}")
        return None

def crop_video(input_file, output_file, start_time, end_time):
    try:
        with VideoFileClip(input_file) as video:
            cropped_video = video.subclip(start_time, end_time)
            cropped_video.write_videofile(output_file, codec='libx264')
        print(f"Cropped video saved to: {output_file}")
    except Exception as e:
        print(f"An error occurred while cropping the video: {e}")

if __name__ == "__main__":
    video_path = "input_video.mp4"
    audio_path = extractAudio(video_path)
    
    if audio_path:
        start_time = 10  # start time in seconds
        end_time = 20    # end time in seconds
        output_video_path = "cropped_video.mp4"
        crop_video(video_path, output_video_path, start_time, end_time)
