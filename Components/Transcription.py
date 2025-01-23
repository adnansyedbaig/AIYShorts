from faster_whisper import WhisperModel
import torch

def transcribeAudio(audio_path, language="en"):
    try:
        print("Transcribing audio...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        model = WhisperModel("base", device=device)  # Use "base" for multilingual support
        print("Model loaded")
        segments, info = model.transcribe(audio=audio_path, beam_size=5, language=language, max_new_tokens=128, condition_on_previous_text=False)
        segments = list(segments)
        extracted_texts = " ".join([segment.text for segment in segments])
        return extracted_texts
    except Exception as e:
        print("Transcription Error:", e)
        return ""

if __name__ == "__main__":
    audio_path = "audio.wav"
    transcriptions = transcribeAudio(audio_path, language="hi")  # Specify "hi" for Hindi
    print("Transcriptions:", transcriptions)
