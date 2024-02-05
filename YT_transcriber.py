import streamlit as st
from dotenv import load_dotenv
import os
import openai
from youtube_transcript_api import YouTubeTranscriptApi

# Function to extract transcript details from a YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([item["text"] for item in transcript_list])
    except Exception as e:
        st.error("Error in extracting transcript: " + str(e))
        return ""

# Function to generate summary using OpenAI's GPT model
def generate_gpt_summary(transcript_text):
    custom_prompt = """
    I am an AI trained to summarize YouTube video content. My task is to extract key points from the video transcript and present them in a concise and informative summary. The summary should encapsulate the main themes and highlights of the video in a structured and easy-to-understand pointwise format. The goal is to provide a comprehensive overview of the video content in about 250 words. The transcript text for summarization is as follows:
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or use "text-davinci-003" based on your preference
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": custom_prompt + transcript_text}
            ],
            max_tokens=250  # Adjust token limit as per your requirement
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        st.error("Error in generating summary: " + str(e))
        return ""

# Load environment variables for OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app layout
st.title("🎥 YouTube Video Summarizer 🌟")

# Input field for YouTube video link
youtube_link = st.text_input("🔗 Paste the YouTube Video Link Here:")

# Displaying thumbnail of the video
if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

# Button to generate summary
if st.button("✨ Create Summary ✨"):
    # Extract transcript details from the YouTube video
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        # Generate summary using OpenAI's GPT model
        summary = generate_gpt_summary(transcript_text)
        st.markdown("## 📝 Video Summary:")
        st.write(summary)
