from transformers import pipeline

# Initialize the Hugging Face summarization model
summarizer = pipeline("summarization", model="google/muril-base-cased")

# Define the system prompt
system_prompt = """
Based on the transcription provided, highlight the main parts in less than 1 minute which can be directly converted into a short video highlight. 
Ensure it includes a clear summary of the key points.
"""

def GetHighlight(Transcription):
    print("Getting Highlight from Transcription ")
    try:
        # Combine the system prompt with the transcription
        prompt = system_prompt + Transcription
        
        # Use the Hugging Face summarizer with the combined prompt
        summary = summarizer(prompt, max_length=60, min_length=10, do_sample=False)
        content = summary[0]['summary_text']
        
        # Mock start and end times (since Hugging Face doesn't provide timestamps)
        start_time = 0
        end_time = 60  # Assume the highlight is 60 seconds long
        
        return start_time, end_time, content
    except Exception as e:
        print(f"Error in GetHighlight: {e}")
        return 0, 0, ""

if __name__ == "__main__":
    User = "Your transcription text goes here."
    start, end, content = GetHighlight(User)
    print(f"Start: {start}, End: {end}, Content: {content}")
