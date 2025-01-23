import os
import ffmpeg

# Ensure 'videos' directory exists
if not os.path.exists('videos'):
    os.makedirs('videos')

def download_youtube_video(youtube_url):
    # Placeholder for actual download logic
    # Assume video_file and audio_file are obtained after download
    video_file = "path_to_video_file.mp4"
    audio_file = "path_to_audio_file.mp3"
    
    output_file = os.path.join('videos', 'output.mp4')
    try:
        stream = ffmpeg.input(video_file)
        audio = ffmpeg.input(audio_file)
        stream = ffmpeg.output(stream, audio, output_file, vcodec='libx264', acodec='aac', strict='experimental')
        ffmpeg.run(stream, overwrite_output=True)

        os.remove(video_file)
        os.remove(audio_file)
    except Exception as e:
        print(f"Error processing video and audio: {e}")
        output_file = video_file

    print(f"Downloaded: {youtube_url} to 'videos' folder")
    print(f"File path: {output_file}")

    # Extract audio and save as audio.wav
    audio_output_path = os.path.join('videos', 'audio.wav')
    try:
        stream = ffmpeg.input(output_file)
        stream = ffmpeg.output(stream, audio_output_path, acodec='pcm_s16le', ac=1, ar='16k')  # Extract audio as WAV
        ffmpeg.run(stream, overwrite_output=True)
    except Exception as e:
        print(f"Error extracting audio: {e}")

    print(f"Extracted audio to: {audio_output_path}")
    return output_file

if __name__ == "__main__":
    youtube_url = input("Enter YouTube video URL: ")
    video_path = download_youtube_video(youtube_url)
    print("Video downloaded to:", video_path)
