import os
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

# ✅ Load the .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ✅ Make sure the API key was actually loaded
if not api_key:
    raise ValueError("OPENAI_API_KEY is missing. Check your .env file.")

client = OpenAI(api_key=api_key)

def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL")

def get_transcript(video_url):
    video_id = get_video_id(video_url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    full_text = " ".join([t['text'] for t in transcript])
    return full_text

def transcript_notes(transcript_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"You're an expert notetaker. From the following YouTube transcript, extract clear, concise notes. Include timestamps **only** when a specific moment is particularly important, such as an example, quote, or insight. Add subheading to make it neat and easy to understand. Make sure to be through and reference youtube video timestamps when necessary!\n\n{transcript_text}"}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content
