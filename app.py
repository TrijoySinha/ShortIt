import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # Load all the environment variables
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("YOUR_API_KEY_HERE"))  # Replace with your actual API key

# Function to get the transcript data from YouTube videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e

# Function to get the summary based on the prompt from Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Streamlit App
st.title("YouTube Video Summarizer")
youtube_link = st.text_input("Enter YouTube Video Link:")

# User can select the summary length
summary_length = st.slider("Select Summary Length (in words):", min_value=50, max_value=500, value=250, step=10)

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        # Update the prompt based on the user's chosen summary length
        prompt = f"You are a YouTube video summarizer. You will summarize the transcript text " \
                 f"and provide the most important points in the summary within {summary_length} words. " \
                 f"Please provide the summary of the text given here: "
        
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)