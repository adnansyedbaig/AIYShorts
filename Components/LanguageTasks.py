from transformers import pipeline

# Initialize the Hugging Face summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Define the system prompt
system_prompt = """
Based on the transcription provided, highlight the main parts in less than 1 minute which can be directly converted into a short video highlight. 
Ensure it includes a clear summary of the key points.
"""

def GetHighlight(transcription):
    print("Getting Highlight from Transcription")
    try:
        # Combine the system prompt with the transcription
        prompt = system_prompt + transcription
        
        # Use the Hugging Face summarizer with the combined prompt
        summary = summarizer(prompt, max_length=60, min_length=10, do_sample=False)
        content = summary[0]['summary_text']
        return content
    except Exception as e:
        print("Error during summarization:", e)
        return ""

if __name__ == "__main__":
    from Transcription import transcribeAudio

    audio_path = "audio.wav"
    transcription = transcribeAudio(audio_path, language="hi")  # Specify "hi" for Hindi
    highlight = GetHighlight(transcription)
    print("Highlight:", highlight)
