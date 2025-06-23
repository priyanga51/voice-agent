import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import os
import time

# Configure Google Gemini API (Replace with your API key)
genai.configure(api_key="YOUR_YOUTUBE_API_KEY")


# Function to capture voice input and convert to text
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the audio."
    except sr.RequestError:
        return "Speech recognition service is unavailable."


# Function to generate AI response using Gemini API
def generate_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"


# Function to convert text to speech and play the response
def speak(text):
    """Convert text to speech and play it."""
    tts = gTTS(text=text, lang="en")
    filename = "response.mp3"

    # Ensure old file is removed before saving a new one
    if os.path.exists(filename):
        os.remove(filename)

    tts.save(filename)
    os.system(f"start {filename}")  # Windows: 'start', macOS: 'afplay', Linux: 'mpg321'

    # Optional: Allow time for the audio to play before deleting
    time.sleep(3)
    os.remove(filename)


# Streamlit UI
st.title("🎙️ AI Voice Agent (Gemini)")
st.write("Click the button below to start speaking!")

if st.button("🎤 Start Listening"):
    user_text = listen()
    if user_text:
        st.write(f"**You said:** {user_text}")
        response = generate_response(user_text)
        st.write(f"**AI Response:** {response}")

        # Speak the response
        speak(response)
